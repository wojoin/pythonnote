# -*- coding: utf-8 -*-
# Package Name  : 
# Project Name  : Python 
# File Name     : anypage
# Author        : 细嗅蔷薇
# Date Time     : 2016/9/20 22:44

from urllib.request import urlopen
from bs4 import BeautifulSoup

import re

import datetime
import random


# 1. 获取页面上的所有链接
def getPage():
    html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
    bsObj = BeautifulSoup(html,"html.parser")

    for link in bsObj.find_all("a"):
        if 'href' in link.attrs:
            print(link.attrs['href'])

# 2. 获取页面上的所有内链接(不指向其他页面的内容)
def getInternalPage():
    html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
    bsObj = BeautifulSoup(html, "html.parser")

    for link in bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            print(link.attrs['href'])



def getLinks(articleUrl):
    random.seed(datetime.datetime.now())
    html = urlopen("http://en.wikipedia.org" + articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

def getInternalPage2():
    links = getLinks("/wiki/Kevin_Bacon")
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
        print("newArticle: " + newArticle)
        links = getLinks(newArticle) # 递归下去
        print("================\r\n")




if __name__ == "__main__":
    # getPage()
    # getInternalPage()
    getInternalPage2()
    print(1)