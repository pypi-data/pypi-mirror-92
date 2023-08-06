# tky

#### 介绍
Tangkaiyue 个人整合方法，python开源仓库；

    本项目是用于记录个人使用的一些Python方法类汇总合集，以方便后续在使用的时候借鉴或复用；
    类似笔记形式，减少后续查找的成本和提高类工作生产力，如对本内容感兴趣的欢迎一起来添砖加瓦；

#### 软件包结构构
````
tky                 |  pip包名
|-  __init__.py
|-  t_sql.py        |  SQL类集合（Oracle/ES...）
|-  t_jde.py        |  判断类集合（判空/匹配...）
|-  t_gui.py        |  GUI类集合（点击/清除/输入/扫描元素...）
|-  t_msg.py        |  消息类集合（企业微信...）
|-  t_file.py       |  文件类集合（Jenkins/文件夹/Excel...）
|-  t_dev.py        |  DEV类集合（APP/PC浏览器...）
````

#### 安装教程

1、pip官源安装： pip install tky    
2、pycharm工具安装：设置-项目-Python解释器-新增包-搜索tky包-安装；

#### 使用说明

工具包在使用时有模块依赖，发现报没模块的异常时，请安装对应的工具包；  
具体的清单以在下方列出；

模块依赖清单：
````
import re, os
import json
import urllib.request
import cx_Oracle
import datetime
import xlrd (建议使用1.2.0的包，支持XLSX格式)
import selenium.webdriver.support.ui as ui
from appium import webdriver
from selenium import webdriver
from xml.dom import minidom
from setuptools import find_packages, setup
from elasticsearch import Elasticsearch, helpers
````

PIP安装指令：
````
pip install re
pip install os
pip install json
pip install urllib
pip install datetime
pip install cx_Oracle == 8.0.1
pip install xlrd  == 1.2.0
pip install selenium == 3.141.0
pip install appium == 0.43
pip install xml.dom
pip install setuptools == 50.3.0
pip install elasticsearch == 7.9.1

PS：包的版本仅为建议项！！！
````
#### 版本日志
     
     版本：1.1.1 【20210127】
        1、修复部分注释对应问题；
        2、GUI方法新增自定义时间参数；
        3、更新部分项目说明；
        
     版本：1.1.0 【20210127】
        1、部分方法测试验证完成，暂未完成完全测试；
        2、修复部分方法调用异常的问题；
        3、新增方法注释；
        4、代码开源，上传至：https://gitee.com/tangkaiyue/tky



#### 参与贡献
欢迎一起参与整合，集合更多的方法调用；

    1、Tangkaiyue （创建仓库/分支，提交代码）

#### 联系作者

````
~~ 【 联 系 方 式 】 ~~
作者：Tang kai yue
企鹅：237736403
主页：tangkaiyue.cn
邮箱：tky_1314@163.com
````
