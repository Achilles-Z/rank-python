#!/usr/bin/python
# -*- coding: utf-8 -*-
# author zeck.tang

import sys
import FileHelper
import datetime

from bs4 import BeautifulSoup
# 热门电视剧 周数据 /hotdrama 是热门电视剧  /?w 是周数据
# http://tv.sohu.com/hotdrama/?w


urls = {
    'hotdrama':'drama',
    'hotmovie':'movie',
    'hotshow':'show',
    'hotcomic':'comic'
}

def getData(keyWord = ''):
    if keyWord == '':
        print 'params lost'
        return False
    todayTime = datetime.date.today()
    targetUrl = 'http://tv.sohu.com/%s' % keyWord
    filePath = FileHelper.getPath(todayTime,'sohu',urls[keyWord])
    fileName = '%s/html.txt' % filePath
    FileHelper.getContent2FileWithoutProcess(fileName=fileName,targetUrl=targetUrl)
    content = open(fileName,'r')
    temp = content.read().decode('utf-8')
    soup = BeautifulSoup(temp,'html.parser')
    count = -1 #过滤第一个
    for tag in soup.findAll(True):
        if tag.has_attr('class'):
            #print ''.join(tag['class'])
            if (''.join(tag['class']) == 'at' and tag.name == 'a') or (tag.name == 'span' and ''.join(tag['class'])  == 'vTotal'):
                count = count + 1
                if count <= 200 and count >= 1 :
                    if count == 1:
                        FileHelper.save2File(content= 'RankDaily \n' , fileName=('%s/RankDaily.txt'% filePath),type= FileHelper.TYPE_APPEND)
                    #日榜数据
                    FileHelper.save2File(content= '%s \n' %tag.string , fileName=('%s/RankDaily.txt'% filePath ) ,type= FileHelper.TYPE_APPEND)
                if count > 200 and count  <= 400 :
                    if count == 201:
                        FileHelper.save2File(content= 'RankWeekly \n' , fileName=('%s/RankWeekly.txt'% filePath ) ,type= FileHelper.TYPE_APPEND)
                    #周榜数据
                    FileHelper.save2File(content= '%s \n' %tag.string , fileName=('%s/RankWeekly.txt'% filePath ) ,type= FileHelper.TYPE_APPEND)
                if count > 400 and count <= 600 :
                    if count == 401:
                        FileHelper.save2File(content= 'RankMonth \n' , fileName=('%s/RankMonthly.txt'% filePath ) ,type= FileHelper.TYPE_APPEND)
                    #月榜数据
                    FileHelper.save2File(content= '%s \n' %tag.string , fileName=('%s/RankMonthly.txt'% filePath ) ,type= FileHelper.TYPE_APPEND)
                if count > 600 :
                    if count == 601:
                        FileHelper.save2File(content= 'RankTotal \n' , fileName=('%s/RankTotal.txt'% filePath ) ,type= FileHelper.TYPE_APPEND)
                    #总计数据
                    FileHelper.save2File(content= '%s \n' %tag.string , fileName=('%s/RankTotal.txt'% filePath) ,type= FileHelper.TYPE_APPEND)
                    #print tag.string

    content.close()
    FileHelper.delFile(fileName)
    #print soup.div
    #print soup.

def getsohuRank():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for keyWord in urls:
        getData(keyWord=keyWord)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for keyWord in urls:
        getData(keyWord=keyWord)