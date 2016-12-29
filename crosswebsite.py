# -*- coding: utf-8 -*-
# Package Name  : 
# Project Name  : Python 
# File Name     : crosswebsite
# Author        : 细嗅蔷薇
# Date Time     : 2016/9/21 19:45

from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("Random external link is:" + externalLink)
    followExternalOnly(externalLink)



def getRandomExternalLink(startingSite):
    html = urlopen(startingSite)
    bsObj = BeautifulSoup(html, "html.parser")
    externalLinks = getExternalLinks(bsObj, urlparse(startingSite).netloc)
    if len(externalLinks) == 0:
        print("No external links, looking around the site for one")
        domain = urlparse(startingSite).scheme + "://" + urlparse(startingSite).netloc  #   获取同一个站点内的链接,domain=https://doc.python.org
        internalLinks = getInternalLinks(bsObj, domain)
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]


#  获取页面所有外链的列表
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    #  找出所有以http或www开头且不包含当前URL的链接
    for link in bsObj.findAll("a",href=re.compile("^(http|www)((?!" + excludeUrl + " ).)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def getInternalLinks(bsObj, includeUrl):
    includeUrl = urlparse(includeUrl).scheme + "://" + urlparse(includeUrl).netloc
    internalLinks = []
    #  找出所有以/开头的链接
    for link in bsObj.findAll("a",href=re.compile("^(/|.*" + includeUrl + ")")):
        if link.arrts['href'] not in internalLinks:
            if(link.attrs['href'].startswith("/")):
                internalLinks.append(includeUrl+link.attrs['href'])
            else:
                internalLinks.append(link.attrs['href'])
    return internalLinks



if __name__ == "__main__":
    urlstring = urlparse("https://docs.python.org/2.7/library/urlparse.html#module-urlparse")
    print("scheme:",urlstring.scheme,"\nnetloc:",urlstring.netloc,"\npath:",urlstring.path,"\nfragment:",urlstring.fragment)

    followExternalOnly("http://oreilly.com")
    print(1)