#!/usr/bin/python
# -*- coding: utf-8 -*-
# author zeck.tang

import requests
import aqy
import re
import json
import sys
import os
import datetime

TYPE_APPEND = 'a'
TYPE_OVERWRITE = 'w'

def getPath (targetDay = '',comp = '' , keyWord = ''):
    if targetDay == '' or comp == '' or keyWord == '':
        print 'params lost'
        return False
    else :
        path = os.getcwd()

        filePath = r'%s/%s/%s/%s' %(path,comp,targetDay,keyWord)
        if os.path.exists(filePath) :
            print 'file Path exists'
        else :
            os.makedirs(filePath)
        return filePath

"""
仅在使用ablumId查询有结果,产生了ids.txt的情况调用
"""
def readVideoIdsfAblum():
    dataFile = open('ids.txt', 'r')
    return json.loads(dataFile.read())

"""
使用ablumId查询,得到ids.txt
"""
def parseAblum(ablumId = ''):
    getContent2File('ablum.txt', aqy.getUrl(videoid=ablumId, type=aqy.ALBUM_TYPE), aqy.ALBUM_TYPE)
    ablumFile = open(name='ablum.txt', mode='r')
    ablumDic = json.loads(ablumFile.read().decode('utf-8'))
    idsFile = open(name='ids.txt', mode='w')
    idsFile.write('{"data":[')
    for i in range(len(ablumDic['data']['vlist'])):
        if i != len(ablumDic['data']['vlist']) -1:
            idsFile.write('{"videoid":%s},' % ablumDic['data']['vlist'][i]['id'])
        else:
            idsFile.write('{"videoid":%s}' % ablumDic['data']['vlist'][i]['id'])
    idsFile.write(']}')
    idsFile.close()
    ablumFile.close()


#提取json数据
"""
从返回内容中截取需要的部分json数据
"""
def extractData(content,type):
    pattern =''
    if type == aqy.COUNT_TYPE:
        pattern = '.*?lfmi\(\[(.*?)\]\);}.*?'
    if type == aqy.PERCENT_TYPE:
        pattern = '.*?MobileCb\((.*?)\);}.*?'
    if type == aqy.INFO_TYPE:
        pattern = '.*?cbvccih6\((.*?),"crumbList".*?'
    if type == aqy.ALBUM_TYPE:
        pattern = '.*?cbs2bcrj\((.*?)\);}.*?'
    items = re.findall(pattern,content)
    #print items[0]
    return items[0]

"""
从目标url获取数据并且存储到指定fileName的txt中
参数说明
fileName : 输出txt文件名 -- 不能为空
targetUrl : 访问目标url -- 不能为空
type : 解析type
"""
def getContent2File(fileName = '',targetUrl = '',type = ''):
    if fileName == '' or targetUrl == '' or type == '':
        print 'params lost'
    else :
        #cookies = cookielib.MozillaCookieJar('cookies.txt')
        content = requests.get(targetUrl)
        #print content.text
        str = extractData(content=content.text,type=type)
        #用覆盖写入方式,省去删除文件和创建文件的内存CPU浪费
        dataFile = open(fileName, 'w')
        if type != aqy.INFO_TYPE:
            dataFile.write(''.join(str).encode('utf-8'))
        else:
            #info的数据是截取的 少2个}}号
            dataFile.write((''.join(str)+'}}').encode('utf-8'))
        dataFile.close()
        print '%s json file saved' % fileName


def getContent2FileWithoutProcess(fileName = '',targetUrl = ''):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if fileName == '' or targetUrl == '':
        print 'params lost'
    else :
        #cookies = cookielib.MozillaCookieJar('cookies.txt')
        content = requests.get(targetUrl)
        #print content.text
        #str = extractData(content=content.text,type=type)
        #用覆盖写入方式,省去删除文件和创建文件的内存CPU浪费
        dataFile = open(fileName, 'w')
        #print content.encoding
        content.encoding = 'utf-8'
        #print content.encoding
        temp = content.text
        dataFile.write(temp)
        dataFile.close()
        print '%s json file saved' % fileName

"""
写数据存储到指定fileName的txt中
参数说明
content : 需写入内容
fileName : 输出txt文件名 -- 不能为空
type : 写文件类型 a | w 追加或覆盖写入
"""
def save2File(fileName = '',type = '',content=''):
    if fileName == '' or type == '':
        print 'params lost'
    else:
        if type == TYPE_APPEND or type == TYPE_OVERWRITE:
            file = open(fileName,type)
            file.write(content.encode('utf-8'))
            file.close()

"""
删除指定文件
参数说明
fileName : 输出txt文件名 -- 不能为空
"""
def delFile(fileName = ''):
    if fileName == '' :
        print 'params lost'
    else:
        if os.path.exists(fileName):
            os.remove(fileName)
            print'file %s removed' % (fileName)
        else :
            print'file %s is not exist' % (fileName)