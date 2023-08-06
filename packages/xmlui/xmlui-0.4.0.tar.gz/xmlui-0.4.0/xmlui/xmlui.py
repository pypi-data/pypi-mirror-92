#!/usr/bin/python
# -*- coding: UTF-8 -*-

from . import xml_ui_tool
import xml.etree.ElementTree as ET

class XmlLoader:
    def load(self, file_or_xmlstring, controllers):
        if "<" in file_or_xmlstring or ">" in file_or_xmlstring:
            self.xml_root = ET.fromstring(file_or_xmlstring)
            self.xml_doc = ET.ElementTree(self.xml_root)
        else:
            self.xml_doc = ET.parse(file_or_xmlstring)
            self.xml_root = self.xml_doc.getroot()

        self.controllers = controllers

        return self.parse_root_element()

class XmlWXLoader(XmlLoader):
    def parse_root_element(self):
        from . import xml_wx
        parser = xml_ui_tool.DocParser(xml_wx.HandleCommonTag)
        parser.controllers = {clas.__name__:clas for clas in self.controllers}
        parser.handle_class = xml_wx.get_all_handle_class()
        handle_app = parser.parse(self.xml_root)
        return handle_app.get_result()

class Controller:
    def __init__(self):
        self.node = None

    def after_load(self):
        pass
