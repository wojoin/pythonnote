# -*- coding: utf-8 -*-
# Package Name  : 
# Project Name  : Python 
# File Name     : website
# Author        : 细嗅蔷薇
# Date Time     : 2016/9/21 8:32

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


# Python默认得递归限制为1000次
# pages = set()
# def getLinks(pageUrl):
#     global pages
#     html = urlopen("http://en.wikipedia.org" + pageUrl)
#     bsObj = BeautifulSoup(html,"html.parser")
#     for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
#         if 'href' in link.attrs:
#             if link.attrs['href'] not in pages:
#                 newPage = link.attrs['href']
#                 print("newPage= " + newPage)
#                 pages.add(newPage)
#                 getLinks(newPage)


pages = set()

def getlinks(pageurl):
    global pages
    html = urlopen("http://en.wikipedia.org" + pageurl)
    bsObj = BeautifulSoup(html, "html.parser")

    try:
        print(bsObj.h1.get_text())  # 标题
        print(bsObj.find(id="mw-content-text").findAll("p")[0])     # 正文得第一个段落
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])    # Edit
    except AttributeError:
        print("页面缺少一些属性,不过不用担心")

    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print("-----------------------------\r\n" + newPage)
                pages.add(newPage)
                getlinks(newPage)


if __name__ == "__main__":
    getlinks("")    # 单个域名的数据采集, 词条采集/wiki/Denial-of-service_attack
    print(1)