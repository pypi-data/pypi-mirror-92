#!/usr/bin/python
# -*- coding: UTF-8 -*-


# 最简单的示例窗口
# 
# 使用环境：
#   python: 3.8
#   wxPython: 4.1.1

import sys
sys.path.append("..")

import xmlui
import wx

class MainController(xmlui.Controller):
    def __init__(self):
        self.doc = None

    def after_load(self):
        self.main_frame.Show(True)

    def OnClickButton(self, evt):
        wx.MessageBox(self.ui_mybtn.GetLabel())

def main():
    loader = xmlui.XmlWXLoader()
    controllers = [MainController]
    wxapp = loader.load("simple_wx.xml", controllers)
    wxapp.MainLoop()

if __name__ == '__main__':
    main()