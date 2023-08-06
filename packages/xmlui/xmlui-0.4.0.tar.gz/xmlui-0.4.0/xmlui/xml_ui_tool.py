#!/usr/bin/python
# -*- coding: UTF-8 -*-

class DocParser:
    def __init__(self, defaultHandleClass):
        self.defaultHandleClass = defaultHandleClass
        self.handle_class = {}
        self.controllers = {}

    def create_controller(self, name):
        return self.controllers[name]()

    def parse(self, xml_element):
        return self.recursive_parse(None, xml_element)

    def recursive_parse(self, handle_parent, xml_element):
        HandleClass = self.handle_class.get(xml_element.tag, None) or self.defaultHandleClass
        handle_obj = HandleClass()

        controller_name = xml_element.get("controller", "").strip()
        if controller_name:
            new_controller = self.create_controller(controller_name)
        else:
            new_controller = None

        handle_obj.init(self, handle_parent, xml_element, new_controller or handle_parent.controller)

        handle_obj.handle()

        name = xml_element.get("name", "").strip()
        if name and handle_obj.get_result() and handle_parent and not hasattr(handle_parent.controller, name):
            setattr(handle_parent.controller, name, handle_obj.get_result())

        handle_obj.handle_over()

        if new_controller:
            setattr(handle_obj.get_result(), "controller", new_controller)
            new_controller.node = handle_obj.get_result()
            new_controller.after_load()

        return handle_obj

class HandleBase:
    def init(self, parser, parent, xml_element, controller):
        self.parser = parser
        self.parent = parent
        self.xml_element = xml_element
        self.controller = controller

        self.ui = None
        self.custom = None
        self.children = []

    def get_result(self):
        return self.ui or self.custom

    def get_latest_ui(self):
        handle_obj = self
        while handle_obj and not handle_obj.ui:
            handle_obj = handle_obj.parent
        if handle_obj:
            return handle_obj.ui

    def handle(self):
        self.handle_self()
        self.handle_children()

    def handle_children(self):
        for child in self.xml_element:
            child_handle_obj = self.parser.recursive_parse(self, child)
            self.children.append(child_handle_obj)
            self.after_handle_child(child_handle_obj)

    def handle_self(self):
        pass

    def after_handle_child(self, child_handle_obj):
        pass

    def handle_over(self):
        pass

def convert_attr_value(attrValue, globals_dict):
    if not attrValue.strip():
        return attrValue
    else:
        try:
            return eval(attrValue, globals_dict)
        except:
            return attrValue