#!/usr/bin/python
# -*- coding: utf-8 -*-
# author zeck.tang

import time
import datetime
import FileHelper
import sys

from bs4 import BeautifulSoup

# 乐视VV(合集) pid =合集id 其余id可无
# http://v.stat.letv.com/vplay/queryMmsTotalPCount?callback=jQuery17105503603010438383_1458892328382&pid=10011988&mid=49409686&cid=2&vid=24910982&_=1458892328565
# 返回内容 plist_play_count即合集播放量
"""
jQuery17105503603010438383_1458892328382({
	"vdm_count": 3076,
	"plist_count": 24,
	"plist_score": 9.4,
	"vcomm_count": 2847,
	"pcomm_count": 8563,
	"preply": 1315,
	"vreply": 360,
	"vnpcomm": 2835,
	"pdm_count": 8994,
	"media_play_count": 2162005,
	"down": 1825,
	"up": 4866,
	"pnpcomm": 8517,
	"plist_play_count": 43911928
})
"""

# 乐视VV(单集)
# getIdsInfo?type=vlist&ids=24910982,24911385,24920292,24920636,24929426,24929794,24930138,24930361&callback=jQuery17105503603010438383_1458892328385&_=1458892328873
# 猜测是单集播放VV
"""
jQuery17105503603010438383_1458892328385([{
	"play_count": 2162005,
	"vreply": 360,
	"id": "24910982",
	"vcomm_count": 2847,
	"up": 4866,
	"down": 1825,
	"dm_count": 3076
}, {
	"play_count": 1982246,
	"vreply": 254,
	"id": "24911385",
	"vcomm_count": 1402,
	"up": 2407,
	"down": 1045,
	"dm_count": 1516
}, {
	"play_count": 992272,
	"vreply": 109,
	"id": "24920292",
	"vcomm_count": 1176,
	"up": 3154,
	"down": 491,
	"dm_count": 1536
}, {
	"play_count": 1297628,
	"vreply": 108,
	"id": "24920636",
	"vcomm_count": 710,
	"up": 1658,
	"down": 497,
	"dm_count": 952
}, {
	"play_count": 706169,
	"vreply": 52,
	"id": "24929426",
	"vcomm_count": 592,
	"up": 1141,
	"down": 246,
	"dm_count": 790
}, {
	"play_count": 1570432,
	"vreply": 132,
	"id": "24929794",
	"vcomm_count": 1069,
	"up": 1550,
	"down": 650,
	"dm_count": 1094
}, {
	"play_count": 510581,
	"vreply": 0,
	"id": "24930138",
	"vcomm_count": 21,
	"up": 253,
	"down": 83,
	"dm_count": 7
}, {
	"play_count": 165854,
	"vreply": 2,
	"id": "24930361",
	"vcomm_count": 37,
	"up": 224,
	"down": 88,
	"dm_count": 11
}])
"""

#href="http://www.le.com


urls = {
    'filmhp':'movie',
    'tvhp':'drama',
    'varhp':'show',
    'comichp':'comic'
}


"""
拼接url
"""
def getUrl(channle = ''):
    if channle == '':
        print 'params lost'
        return False
    else:
        return 'http://top.le.com/%s.html' % channle

def getData(keyWord = ''):
    targetUrl = getUrl(keyWord)
    todayTime = datetime.date.today()
    filePath = FileHelper.getPath(todayTime,'letv',urls[keyWord])
    fileName = '%s/html.txt' % filePath
    FileHelper.getContent2FileWithoutProcess(fileName=fileName,targetUrl=targetUrl)
    content = open(fileName,'r')
    temp = content.read().decode('utf-8')
    soup = BeautifulSoup(temp,'html.parser')
    rank = 0
    for tag in soup.findAll(True):
        # 每50条为分割
        if(tag.name == 'a' and tag.has_attr('href') and (''.join(tag['href']).find('www.le.com') > 0) and rank<150):
            rank = rank + 1
            if rank <= 50:
                FileHelper.save2File(content = 'Rank.%s %s ' % (rank,tag.string ), fileName='%s/RankDaily.txt' % filePath,type= FileHelper.TYPE_APPEND)
            if rank <=100 and rank >50:
                FileHelper.save2File(content = 'Rank.%s %s ' % (rank-50,tag.string ), fileName='%s/RankWeekly.txt' % filePath,type= FileHelper.TYPE_APPEND)
            if rank <= 150 and rank > 100:
                FileHelper.save2File(content = 'Rank.%s %s ' % (rank-100,tag.string ), fileName='%s/RankMonthly.txt' % filePath,type= FileHelper.TYPE_APPEND)

        if (tag.has_attr('class') and tag.name == 'span' and ''.join(tag['class']) == 't-5'  and rank<150):
            if rank <= 50:
                FileHelper.save2File(content = 'VV : %s \n' % tag.string , fileName='%s/RankDaily.txt' % filePath,type= FileHelper.TYPE_APPEND)
            if rank <=100 and rank >50:
                FileHelper.save2File(content = 'VV : %s \n' % tag.string , fileName='%s/RankWeekly.txt' % filePath,type= FileHelper.TYPE_APPEND)
            if rank <= 150 and rank > 100:
                FileHelper.save2File(content = 'VV : %s \n' % tag.string , fileName='%s/RankMonthly.txt' % filePath,type= FileHelper.TYPE_APPEND)

    content.close()
    FileHelper.delFile(fileName)

def getletvRank():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for keyWord in urls.keys():
        getData(keyWord=keyWord)
        time.sleep(1)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for keyWord in urls.keys():
        getData(keyWord=keyWord)
        time.sleep(1)