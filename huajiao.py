# -*- coding: utf-8 -*-
# Project Name  :  
# File Name     : 
# Author        : 细嗅蔷薇
# Date Time     : 2016/12/27 16:49
# Description   :
# Version       : 1.0.1
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import json
import datetime
import csv


# 1. 从直播列表(一个类别)页过滤处直播Id列表
DOMAIN = "http://www.huajiao.com"

def filterLiveId(url):
    liveIds = set()
    html = urlopen(url)
    bsObj = BeautifulSoup(html, "html.parser")
    for link in bsObj.findAll("a",href=re.compile("^(/l/)")):
        if "href" in link.attrs:
            if link.attrs["href"] not in liveIds:
                newPage = link.attrs["href"]
                liveId = re.findall("[0-9]+", newPage)
                liveIds.add(liveId[0])
    #print(liveIds)
    return liveIds

#1.1 从【热门推荐】类别获取其他页面的主播Id列表
def getLiveIdsFromRecommendPage():
    liveId = set()
    liveId = filterLiveId("http://www.huajiao.com/category/1000") | filterLiveId("http://www.huajiao.com/category/1000?pageno=2")
    return liveId

# 2.从直播页过滤出主播id
def getUserId(liveId):

    html = urlopen(DOMAIN+"/l/"+str(liveId))
    bsObj = BeautifulSoup(html, "html.parser")
    useridlink = bsObj.find(id="author-info").find("a",href=re.compile("^(/user/)"))
    if useridlink.attrs["href"] is not None:
        userId = re.findall("[0-9]+",useridlink.attrs["href"])[0]
        #print(userId)
        return userId

# 3.通过userId进入主播个人主页获取个人信息
def getUserInfo(userId):
    userId = str(userId)
    html = urlopen(DOMAIN + "/user/" +  userId)
    bsObj = BeautifulSoup(html, "html.parser")
    data = dict()
    try:
        userInfo = bsObj.find("div", {"id":"userInfo"})
        data['avatar'] = userInfo.find("div",{"class":"avatar"}).img.attrs['src']
        userId = userInfo.find("p", {"class":"user_id"}).get_text()
        data['userid'] = re.findall("[0-9]+",userId)
        tmp = userInfo.h3.get_text('|', strip=True).split('|') # 适用于存在内嵌子标签的元素
        data['username'] = tmp[0]
        data['level'] = tmp[1]
        tmp = userInfo.find("ul",{"class":"clearfix"}).get_text('|', strip=True).split('|')
        data['follow'] = tmp[0]
        data['fans'] = tmp[2]
        data['support'] = tmp[4]
        data['experience'] = tmp[6]
        return data
    except AttributeError:
        print(str(userId) + "error")
        return 0

# 4.将获取的个人信息写入mysql
# def replaceUserData(data):
#      conn = getMysqlConn()
#      cur = conn.cursor()
#      try:
#          cur.execute("USE wanghong")
#          cur.execute("set names utf8mb4")
#          cur.execute("REPLACE INTO Tbl_Huajiao_User(FUserId,FUserName, FLevel, FFollow,FFollowed,FSupported,FExperience,FAvatar,FScrapedTime) "
#                      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#                      (int(data['userid']), data['username'],int(data['level']),int(data['follow']),int(data['fans']),
#                       int(data['supported']), int(data['experience']), data['avatar'],datetime.datetime.now())
#          )
#          conn.commit()
#      except pymysql.err.InternalError as e:
#          print(e)


# 5.获取某直播历史数据
def getUserLives(userId):
    try:
        url = "http://webh.huajiao.com/User/getUserFeeds?fmt=json&amp;uid=" + str(userId)
        html = urlopen(url).read().decode('utf-8')
        jsonData = json.loads(html)
        if jsonData['errno'] != 0:
            print(str(userId) + "error occured in getUserFeeds for: " + jsonData['msg'])
            return 0
        return jsonData['data']['feeds']
    except Exception as e:
        print(e)
        return 0

# 爬虫的主要函数
# 1.爬去用户信息
def spiderUserDatas():
    users = []
    for liveId in getLiveIdsFromRecommendPage():
        userId = getUserId(liveId)
        userData = getUserInfo(userId)
        users.append(userData)
        # if userData:
        #     print(userData) # 写入DB
            # with open('huajiao.txt','a',encoding="utf-8") as fp:
            #     fp.write(str(userData))
            #     fp.write("\n")
    print(users)
    print("*"*100)
    print(sorted(users,key=lambda k:k['level'])) # 按照level排序

    for u in users:
        with open('huajiao.txt','a',encoding='utf-8') as fp:
            fp.write(str(u))
            fp.write("\r\n")


    # for u in users:
    #     with open('huajiao.csv', 'a', newline='',encoding='utf-8') as csvfile:
    #         writer = csv.writer(csvfile)
    #         writer.writerow(str(u)+"\n")


if __name__ == "__main__":
    # url = "http://www.huajiao.com/category/1000"
    # print(filterLiveId(url))
    #
    # liveId = "62698605" # 62569901
    # print(getUserId(liveId))
    #
    # print("*"*100)
    # userid = "24172309"
    # getUserInfo(userid)

    spiderUserDatas()
    print(1)

    # lis = [
    #     {'x': 3, 'y': 2, 'z': 1},
    #     {'x': 2, 'y': 1, 'z': 3},
    #     {'x': 1, 'y': 3, 'z': 2},
    # ]
    # print(sorted(lis, key=lambda k: k['x']))
    #
    # fp = open('huajiao.txt', 'w', encoding='utf-8')
    # for u in lis:
    #     fp.write(str(u))
    #     fp.write("\r\n")
    # fp.close()
    # print(csv.list_dialects())
    # with open('eggs.csv','w',newline='') as csvfile:
    #     writer = csv.writer(csvfile,delimiter=' ',quotechar=',',quoting=csv.QUOTE_MINIMAL)
    #     writer.writerow(['Spam']*5+['Black Beans'])
    #     writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
