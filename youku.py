#!/usr/bin/python
# -*- coding: utf-8 -*-
# author zeck.tang


import sys
import FileHelper
import datetime
import time
from bs4 import BeautifulSoup

# 优酷VV
# http://v.youku.com/QVideo/~ajax/getVideoPlayInfo?__rt=1&__ro=&id=376597544&sid=304175&type=vv&catid=85

# 优酷推荐
# http://ykrec.youku.com/show/packed/list.json?guid=14581113301817Oz&vid=374753616&sid=304175&cate=85&apptype=1&pg=3&module=1&pl=20&needTags=0&picSize=2&atrEnable=true&callback=RelationAsync.likeShowCallback&t=0.744534989813792

# 合集播放
#<span class="play"><label>总播放:</label>692,215,867</span>

# 电视剧热度排行
# http://www.youku.com/v_olist/c_97_s_1_d_2.html
# c_97是电视剧频道 c_96是电影 以此类推,
# s_1是排序第一个参数 播放次数 s_2是评论条数
# d_1是排序第二个参数 今日播放量 d_2是本周播放量  d_4是历史播放量
# c_97_g__a__sg__mt__lg__q__s_1_r_0_u_0_pt_0_av_0_ag_0_sg__pr__h__d_1_p_3 最后一个 p_3表示第三页 p_x表示第X页.第一页可以不用传
#url = 'http://www.youku.com/v_olist/c_97.html'

urls = {
    'c_97':'drama',
    'c_96':'movie',
    'c_85':'show',
    'c_100':'comic'
}

TYPE_DAILY = 'daily'
TYPE_WEEKLY = 'weekly'
"""
拼接url
"""
def getUrl(channle = '',page = -1,type =''):
    if channle == '' or page == -1 or type == '':
        print 'params lost'
        return False
    else:
        if page <= 1 :
            if type == TYPE_DAILY:
                return 'http://www.youku.com/v_olist/%s.html' % channle
            if type == TYPE_WEEKLY:
                return 'http://www.youku.com/v_olist/%s_s_1_d_2.html' % channle
        else:
            if type == TYPE_DAILY:
                return 'http://www.youku.com/v_olist/%s_g__a__sg__mt__lg__q__s_1_r_0_u_0_pt_0_av_0_ag_0_sg__pr__h__d_1_p_%s.html' % (channle,page)
            if type == TYPE_WEEKLY:
                return 'http://www.youku.com/v_olist/%s_g__a__sg__mt__lg__q__s_1_r_0_u_0_pt_0_av_0_ag_0_sg__pr__h__d_2_p_%s.html' % (channle,page)

def getData(keyWord = '',page = -1,type = ''):
    targetUrl = getUrl(keyWord,page,type)
    todayTime = datetime.date.today()
    filePath = FileHelper.getPath(todayTime,'youku',urls[keyWord])
    fileName = '%s/html.txt' % filePath
    FileHelper.getContent2FileWithoutProcess(fileName=fileName,targetUrl=targetUrl)
    content = open(fileName,'r')
    temp = content.read().decode('utf-8')
    soup = BeautifulSoup(temp,'html.parser')
    rank = (page - 1) * 42 #一页42个数据
    resultFileName=''
    if type == TYPE_DAILY:
        resultFileName='%s/RankDaily.txt' % filePath
    if type == TYPE_WEEKLY:
        resultFileName='%s/RankWeekly.txt' % filePath
    for tag in soup.findAll(True):
        if(tag.name == 'img' and tag.has_attr('alt') and tag.has_attr('src') and not tag.has_attr('attr')):
            rank = rank+1
            FileHelper.save2File(content = 'Rank.%s %s ' % (rank,tag['alt'] ), fileName=resultFileName,type= FileHelper.TYPE_APPEND)
        if (tag.has_attr('class') and tag.name == 'span' and ''.join(tag['class']) == 'p-num'):
            FileHelper.save2File(content = 'VV : %s \n' % tag.string , fileName=resultFileName,type= FileHelper.TYPE_APPEND)

    content.close()
    FileHelper.delFile(fileName)
#span class="p-num"
#p-meta-title

def getyoukuRank():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for keyWord in urls.keys():
        getData(keyWord=keyWord,page=1,type=TYPE_DAILY)
        time.sleep(1)
        getData(keyWord=keyWord,page=2,type=TYPE_DAILY)
        time.sleep(1)
        getData(keyWord=keyWord,page=3,type=TYPE_DAILY)
        time.sleep(1)
    for keyWord in urls.keys():
        getData(keyWord=keyWord,page=1,type=TYPE_WEEKLY)
        time.sleep(1)
        getData(keyWord=keyWord,page=2,type=TYPE_WEEKLY)
        time.sleep(1)
        getData(keyWord=keyWord,page=3,type=TYPE_WEEKLY)
        time.sleep(1)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for keyWord in urls.keys():
        getData(keyWord=keyWord,page=1,type=TYPE_DAILY)
        time.sleep(1)
        getData(keyWord=keyWord,page=2,type=TYPE_DAILY)
        time.sleep(1)
        getData(keyWord=keyWord,page=3,type=TYPE_DAILY)
        time.sleep(1)
    for keyWord in urls.keys():
        getData(keyWord=keyWord,page=1,type=TYPE_WEEKLY)
        time.sleep(1)
        getData(keyWord=keyWord,page=2,type=TYPE_WEEKLY)
        time.sleep(1)
        getData(keyWord=keyWord,page=3,type=TYPE_WEEKLY)
        time.sleep(1)



