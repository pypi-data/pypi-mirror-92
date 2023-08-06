#encoding=utf8

from setuptools import setup, find_packages

setup(
    name = "xmlui",
    version = "0.4.0",
    keywords = ["pip", "wx","tkinter", "xml"],
    description = "基于tkinter和wxPython,使用xml描述ui结构的二次开发库",
    long_description = "借鉴了html的方式，通过xml描述UI结构",
    license = "MIT Licence",

    url = "https://gitee.com/zhangdianwei/xmlui.git",
    author = "zhang",
    author_email = "2317365219@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["wxPython"]
)
