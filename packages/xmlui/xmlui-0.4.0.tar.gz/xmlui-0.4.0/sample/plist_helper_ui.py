#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 修改TexturePacker导出的.plist的GUI工具
# 支持替换小图、导出小图、调用TexturePacker再次打包
# 
# 使用方式：
#   1.将plist文件拖拽到窗口内打开
#   2.将png文件拖拽到窗口内修改
#   3.点击保存
# 
# 
# 使用环境：
#   python: 3.8
#   xmlui: 0.3
#   wxPython: 4.1.1
#   TexturePacker: 5.4

import sys
sys.path.append("..")

import xmlui
import wx
import os
import plistlib
import re
import shutil
import stat

class PlistFrame:
    def FromConfig(config):
        ret = PlistFrame()
        ret.config = config

        match = re.match(r"{{(\d+),(\d+)},{(\d+),(\d+)}}", config["textureRect"])
        x,y,w,h = match.group(1),match.group(2),match.group(3),match.group(4)
        x,y,w,h = int(x),int(y),int(w),int(h)
        ret.textureRect = wx.Rect(x, y, w, h)
        
        ret.bitmap = None
        ret.state = None

        return ret

    def FromNew(bitmap):
        ret = PlistFrame()
        ret.textureRect = None
        ret.bitmap = bitmap
        ret.state = "[+]"
        return ret

class PlistDoc:
    def __init__(self, plistname):
        self.plistname = plistname
        self.imagename = self.plistname.replace(".plist", ".png")
        self.image = None
        self.bitmap = None
        self.frames = None
        self.ReloadPlistContent(self.plistname, self.imagename)

    def Replace(self, name, bitmap):
        self.frames[name].bitmap = bitmap
        self.frames[name].state = "[M]"
    def AddFrame(self, name, bitmap):
        self.frames[name] = PlistFrame.FromNew(bitmap)

    def ReloadPlistContent(self, plistname, imagename):
        image = wx.Image(imagename)
        bitmap = image.ConvertToBitmap()

        frames = {}
        plist = plistlib.readPlist(plistname)
        for name,config in plist["frames"].items():
            frames[name] = PlistFrame.FromConfig(config)
            if self.frames and name in self.frames:
                frames[name].state = self.frames[name].state

        self.image = image
        self.bitmap = bitmap
        self.frames = frames

    def RefreshByTexturePacker(self):
        tmpDir = "tmp"
        outplist = os.path.join(tmpDir, "tmp.plist")
        if not self.SaveTo(tmpDir, outplist):
            return
        self.ReloadPlistContent(outplist, outplist.replace(".plist", ".png"))
        shutil.rmtree(tmpDir)

    def IsModified(self):
        for name, frame in self.frames.items():
            if frame.state=="[M]": return True
            if frame.state=="[+]": return True
        return False

    def HasNewFrame(self):
        for name, frame in self.frames.items():
            if frame.state=="[+]": return True
        return False

    def ExportTo(self, tmpDir):
        if os.path.isdir(tmpDir):
            shutil.rmtree(tmpDir)
        os.mkdir(tmpDir)
        for name, frame in self.frames.items():
            if frame.bitmap:
                bmp = frame.bitmap
            else:
                bmp = self.bitmap.GetSubBitmap(frame.textureRect)
            bmp.SaveFile(os.path.join(tmpDir, name), wx.BITMAP_TYPE_PNG)

    def SaveTo(self, tmpDir, outplist):
        self.ExportTo(tmpDir)

        cmd = "TexturePacker %s --format cocos2d --data %s"%(tmpDir, outplist)
        ret = os.system(cmd)
        if ret != 0:
            wx.MessageBox(cmd+":"+str(ret), "error")
            return

        return True

    def Save(self):
        if not self.IsModified():
            wx.MessageBox("没有修改，无法保存", "错误")
            return

        tmpDir = "tmp"

        if not self.SaveTo(tmpDir, self.plistname):
            return

        shutil.rmtree(tmpDir)

        self.ReloadPlistContent(self.plistname, self.imagename)
        for name, frame in self.frames.items():
            frame.state = None

        wx.MessageBox("已经保存到:%s"%(self.plistname), "成功")
        return True


    def NeedTexturePacker(self):
        for name, frame in self.frames.items():
            if not frame.bitmap: continue
            if frame.textureRect.GetSize()!=frame.bitmap.GetSize():
                return True
        return False

    def Draw(self, dc):
        topLeft = wx.Point(wx.Point()-self.bitmap.GetSize()/2)

        dc.DrawBitmap(self.bitmap, topLeft.x, topLeft.y)

        for name, frame in self.frames.items():
            if not frame.bitmap: continue
            dc.DrawBitmap(frame.bitmap, topLeft.x+frame.textureRect.GetX(), topLeft.y+frame.textureRect.GetY())


MY_EVT_SCALE_PLISTDRAW = wx.NewEventType()
MY_EVT_SCALE_PLISTDRAW_BINDER = wx.PyEventBinder(MY_EVT_SCALE_PLISTDRAW)

EVT_DROPFILES = wx.NewEventType()
EVT_DROPFILES_BINDER = wx.PyEventBinder(EVT_DROPFILES)

class MainFrameDropTarget(wx.FileDropTarget):
    def __init__(self, mainController):
        wx.FileDropTarget.__init__(self)
        self.mainController = mainController

    def OnDropFiles(self, x, y, filenames):
        if self.CheckPlist(filenames):
            return True

        if not self.mainController.doc:
            return True

        replacefiles = []
        newfiles = []
        for fullname in filenames:
            if not fullname.lower().endswith(".png"): continue
            fpath, fname = os.path.split(fullname)
            if self.mainController.doc.frames.get(fname):
                replacefiles.append(fullname)
            else:
                newfiles.append(fullname)

        for fullname in replacefiles:
            fpath, fname = os.path.split(fullname)
            bitmap = wx.Image(fullname).ConvertToBitmap()
            self.mainController.doc.Replace(fname, bitmap)


        if not self.mainController.ui_allownew.GetValue() and len(newfiles)>0:
            wx.MessageBox("如果要添加新图，先勾选允许添加新图")
            
        if self.mainController.ui_allownew.GetValue():
            for fullname in newfiles:
                fpath, fname = os.path.split(fullname)
                bitmap = wx.Image(fullname).ConvertToBitmap()
                self.mainController.doc.AddFrame(fname, bitmap)

        if len(newfiles)>0 and self.mainController.ui_allownew.GetValue():
            self.mainController.doc.RefreshByTexturePacker()
        self.mainController.Refresh()
        return True

    def CheckPlist(self, filenames):
        fullname = filenames[0]
        if not fullname.lower().endswith(".plist"):
            return False
        self.mainController.LoadPlist(fullname)
        return True


class PlistDrawController(xmlui.Controller):
    def __init__(self):
        self.doc = None
        self.downPos = None
        self.selectedFrame = None
        self.scale = 1
        self.center = None

    def SetDoc(self, doc):
        self.doc = doc
        self.ResetView()

    def PlaceCenterAt(self, pos):
        self.center = pos
        self.Refresh()

    def SetScale(self, scale):
        self.scale = scale
        self.Refresh()

    def ResetView(self):
        self.scale = 1
        self.center = wx.Point()+self.node.GetClientSize()/2
        self.Refresh()

    def Refresh(self):
        self.node.Refresh()

    def SelectFrame(self, frame):
        self.selectedFrame = frame

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self.node)
        dc.Clear()

        if self.doc:
            topLeft = wx.Point(wx.Point()-self.doc.bitmap.GetSize()/2)

            origin = wx.Point()+self.node.GetClientSize()/2
            dc.SetDeviceOrigin(self.center.x, self.center.y)
            dc.SetUserScale(self.scale, self.scale)
            self.doc.Draw(dc)

            dc.SetPen(wx.Pen(wx.Colour(255,0,0), 2))
            dc.SetBrush(wx.Brush(wx.Colour(0,0,0), wx.BRUSHSTYLE_TRANSPARENT))
            dc.DrawRectangle(topLeft, self.doc.bitmap.GetSize())

            if self.selectedFrame:
                dc.SetPen(wx.Pen(wx.Colour(0,255,0), 2))
                dc.SetBrush(wx.Brush(wx.Colour(0,255,0), wx.BRUSHSTYLE_BDIAGONAL_HATCH))
                frame = self.doc.frames[self.selectedFrame]
                dc.DrawRectangle(frame.textureRect.GetPosition()+topLeft, frame.textureRect.GetSize())

    def OnMouseDown(self, evt):
        self.node.CaptureMouse()
        self.downPos = evt.GetPosition()
        self.Refresh()
    def OnMouseUp(self, evt):
        if self.downPos:
            self.node.ReleaseMouse()
            self.downPos = None
        self.Refresh()
    def OnMouseWheel(self, evt):
        diff = evt.GetWheelRotation()/120/10
        event = wx.PyCommandEvent(MY_EVT_SCALE_PLISTDRAW, self.node.GetId())
        event.scale = self.scale+diff
        self.node.GetEventHandler().ProcessEvent(event)

    def OnMouseMove(self, evt):
        if not self.downPos:
            return
        if not self.center:
            return

        vec = evt.GetPosition()-self.downPos
        target = self.center+vec
        self.PlaceCenterAt(target)
        self.downPos = evt.GetPosition()

    def after_load(self):
        pass

class MainController(xmlui.Controller):
    def __init__(self):
        self.doc = None
    def after_load(self):
        self.main_frame.Show(True)
        self.main_frame.SetDropTarget(MainFrameDropTarget(self))
        self.ui_draw.Bind(MY_EVT_SCALE_PLISTDRAW_BINDER, self.OnSetScale, id=self.ui_draw.GetId())
        self.RefreshFileTree(None)

    def LoadPlist(self, plistname):
        if self.doc and self.doc.IsModified():
            if wx.MessageBox("当前文件未保存，确认打开新文件？",style=wx.YES_NO|wx.ICON_QUESTION)!=wx.YES:
                return
        self.ui_allownew.SetValue(False)
        
        self.doc = PlistDoc(plistname)
        self.ui_draw.controller.SetDoc(self.doc)
        self.SetScale(100)
        self.Refresh()

    def Refresh(self):
        self.ui_plistcontent.Clear()
        if self.doc:
            for name, frame in self.doc.frames.items():
                index = self.ui_plistcontent.Append(name)

        self.ui_draw.controller.Refresh()

    def SetScale(self, scaleValue):
        scale = int(scaleValue)
        if scale<self.ui_scaleSlider.GetMin():
            scale = self.ui_scaleSlider.GetMin()
        elif scale>self.ui_scaleSlider.GetMax():
            scale=self.ui_scaleSlider.GetMax()
        self.ui_scaleSlider.SetValue(scale)
        self.OnScaleChanged(None)

    def AddTreeItem(self, treeItem, rootpath, pattern):
        if self.ui_filetree.GetCount()>200:
            return
        for name in os.listdir(rootpath):
            if name.startswith(".") or name.startswith("_"):
                continue
            fullpath = os.path.join(rootpath, name)
            if os.path.isdir(fullpath):
                child = self.ui_filetree.AppendItem(treeItem, name)
                self.AddTreeItem(child, fullpath, pattern)
            elif os.path.isfile(fullpath) and name.lower().endswith(".plist") and pattern in name:
                child = self.ui_filetree.AppendItem(treeItem, name)
                self.ui_filetree.SetItemData(child, fullpath)
                self.ui_filetree.SetItemBold(child, True)

    def RefreshFileTree(self, pattern):
        if not pattern:
            pattern = ""
        if pattern:
            pattern = pattern.strip().lower()

        rootPath = r"D:\zproj\xmlui\sample"

        self.ui_filetree.DeleteAllItems()
        root = self.ui_filetree.AddRoot(rootPath)
        if not os.path.isdir(rootPath):
            return
        self.AddTreeItem(root, rootPath, pattern)

        if pattern:
            self.ui_filetree.ExpandAll()
        else:
            self.ui_filetree.ExpandAllChildren(root)

    def OnClickReset(self, evt):
        self.ui_draw.controller.ResetView()
        self.ui_scaleSlider.SetValue(100)
    def OnSelectPlistFrame(self, evt):
        self.ui_draw.controller.SelectFrame(evt.GetString())
        self.ui_draw.controller.Refresh()
    def OnScaleChanged(self, evt):
        self.ui_draw.controller.SetScale(self.ui_scaleSlider.GetValue()/100)
    def OnSetScale(self, evt):
        self.SetScale(evt.scale*100)
    def OnClickSave(self, evt):
        if not self.doc: return
        if not self.doc.Save():
            return
        # self.LoadPlist(self.doc.plistname)
        self.Refresh()
    def OnClickExport(self, evt):
        if not self.doc: return
        savePath = wx.DirSelector("保存路径")
        if savePath:
            self.doc.ExportTo(savePath)
    def OnSearchChanged(self, evt):
        self.RefreshFileTree(evt.GetString())
    def OnFileTreeSelected(self, evt):
        path = self.ui_filetree.GetItemData(evt.GetItem())
        if path:
            self.LoadPlist(path)

def main():
    loader = xmlui.XmlWXLoader()
    controllers = [MainController, PlistDrawController]
    wxapp = loader.load("xml_wx.xml", controllers)
    wxapp.MainLoop()

if __name__ == '__main__':
    main()