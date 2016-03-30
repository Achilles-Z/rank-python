#!/usr/bin/python
# -*- coding: utf-8 -*-
# author zeck.tang

import dataMix
import json
import FileHelper
import sys
import datetime
import time
from bs4 import BeautifulSoup
#视频信息
#http://cache.video.qiyi.com/jp/vi/453406400/778e9e5286f2ca6a94d8b5da0062f978/?status=1&callback=window.Q.__callbacks__.cbyexhk1

#playcount
#url ='http://cache.video.qiyi.com/jp/pc/202938201/?src=760859ef3a0046e0932d0381e641cbb6&callback=window.Q.__callbacks__.cby7lfmi'
#url = 'http://cache.video.qiyi.com/jp/pc/462644800,462617400,462614900,462482600,462302600,462301400,461713200,461713000,461469500,461359700,461234800,461039700,461037300,461035200,461027300,461026600,460957400,460958800,460957300,460956300,460957000,460955700,460957800,460943500,460949500,460948200,460947700,460946300,460945700,460800100,460797600,460789700,460783000,460775100,460772100,460770300,460738800,460613800,460613100,460354500,460144400,459903900,459142300,459752500,459598300,459546900,459546300,459385600,459382900,459036400,458733900,458568500,458561000,458556000,458554100,458184400,458335800,458331200,458283400,458157400,458157300,458152000,458149900,458125700,457878100,457562900,457541000,457322300,457230000,457092600,456906100,456640300,456572600,456484700,456188900,456214000,456213700,456208800,455945900,455837900,455814600,455811400,455806300,455738200,454976900,454976300,454975700,454973100,454969800,454969000,454910600,454909700,454873800,454822200,454530500,453816900,453543700,453438000,453332600,453074400,452949400,452949100,452948600,452948300,452947800,452792000,452785200,451191100,451083400,450915200,449657200,448772500,446049900,443683000,441430400,439106100,436284800,435403800,433991700/?src=760859ef3a0046e0932d0381e641cbb6&callback=window.Q.__callbacks__.cbr2s58y'
#url = 'http://cache.video.qiyi.com/jp/pc/462644800,462617400/?src=760859ef3a0046e0932d0381e641cbb6&callback=window.Q.__callbacks__.cbqjvlli'

#video information
#url = 'http://cache.video.qiyi.com/jp/vi/461297400/5028d0314622a72033953443ac146284/?status=1&callback=window.Q.__callbacks__.cbb4axsk'

#点赞数
#url = 'http://up.video.iqiyi.com/ugc-updown/quud.do?dataid=461297400&type=2&userid=&flashuid=8d54f4ec14ed1068283eb09fe237e1e7&appID=21&callback=window.Q.__callbacks__.cbvbjj22'

#评论 返回结果尾部会有count
#url ='http://cmts.iqiyi.com/comment/tvid248/13545243_461297400_hot_2?is_video_page=true&qypid=01010011010000000000&albumid=461297400&t=0.17953874776139855&callback=window.Q.__callbacks__.hot_13545243_461297400'

#移动 /PC 占比
#url = 'http://cache.video.qiyi.com/pc/pr/461297400/playCountPCMobileCb?callback=playCountPCMobileCb'
#try{playCountPCMobileCb({"code":"A00000","data":{"p":12,"f":2,"m":88}});}catch(e){}; //p是pc,m是mobile

#合集下剧集info
#http://cache.video.qiyi.com/jp/avlist/202938201/1/50/?albumId=202938201&pageNo=1&pageNum=50&callback=window.Q.__callbacks__.cbs2bcrj

#热搜榜单url
#http://search.video.qiyi.com/m?cb=cb_HOwaHbP6LeK5UdjWVy9DN3t2H362uSJHVoGY&if=hotQuery&p=global

"""
baseurl = 'http://cache.video.qiyi.com/jp/pc/'
COUNT_TYPE ='count'
PERCENT_TYPE ='percent'
INFO_TYPE = 'info'
ALBUM_TYPE = 'album'

#拼接url 替换videoid
def getUrl(videoid = '',type = ''):
    if videoid == '' or type == '':
        print 'params lost'
    else :
        if type == COUNT_TYPE:
            return 'http://cache.video.qiyi.com/jp/pc/%s/?src=760859ef3a0046e0932d0381e641cbb6&callback=window.Q.__callbacks__.cby7lfmi' % videoid
        if type == PERCENT_TYPE:
            return 'http://cache.video.qiyi.com/pc/pr/%s/playCountPCMobileCb?callback=playCountPCMobileCb' % videoid
        if type == INFO_TYPE:
            return 'http://mixer.video.iqiyi.com/jp/mixin/videos/%s?callback=window.Q.__callbacks__.cbvccih6&status=1' % videoid
            #return 'http://cache.video.qiyi.com/jp/vi/%s/778e9e5286f2ca6a94d8b5da0062f978/?status=1&callback=window.Q.__callbacks__.cbyexhk1' % videoid
        if type == ALBUM_TYPE:
            return 'http://cache.video.qiyi.com/jp/avlist/%s/1/50/?albumId=%s&pageNo=1&pageNum=50&callback=window.Q.__callbacks__.cbs2bcrj' % (videoid,videoid)



if __name__ == '__main__':
    #202909701 山海经
    #202938201 太阳的后裔
    FileHelper.parseAblum('202909701')
    dicIds = FileHelper.readVideoIdsfAblum()
    print len(dicIds['data'])
    for i in range(0,len(dicIds['data'])):
        videoid = dicIds['data'][i]['videoid']
        FileHelper.getContent2File('percent.txt', getUrl(videoid=videoid, type=PERCENT_TYPE), PERCENT_TYPE)
        FileHelper.getContent2File('info.txt', getUrl(videoid=videoid, type=INFO_TYPE), INFO_TYPE)
        dataMix.mixData(videoid)

"""


urls = {
    '1':'movie',
    '2':'drama',
    '6':'show',
    '4':'comic'
}

TYPE_DAILY = 'day'
TYPE_WEEKLY = 'wee'
TYPE_TOTAL = 'his'

"""
拼接url
"""
def getUrl(channle = '',type = ''):
    if channle == '' or type == '':
        print 'params lost'
        return False
    else:
        return 'http://top.inter.qiyi.com/index/front?cid=%s&dim=%s&len=50&area=top' % (channle,type)
# http://top.inter.qiyi.com/index/front?cid=2&dim=day&len=50&area=top
# cid = 2 电视剧 cid = 4 动漫 cid = 6 综艺 cid = 1 电影

def getData(keyWord = '',type = ''):
    targetUrl = getUrl(keyWord,type)
    todayTime = datetime.date.today()
    filePath = FileHelper.getPath(todayTime,'aqy',urls[keyWord])
    fileName = '%s/json.txt' % filePath
    FileHelper.getContent2FileWithoutProcess(fileName=fileName,targetUrl=targetUrl)
    content = open(fileName,'r')
    temp = content.read().decode('utf-8')
    dic = json.loads(temp)
    key = ''
    resultFileName = ''
    if type == TYPE_DAILY:
        resultFileName='%s/RankDaily.txt' % filePath
        key = 'album_count_yesterday'
    if type == TYPE_WEEKLY:
        resultFileName='%s/RankWeekly.txt' % filePath
        key = 'album_count_lastweek'
    count = len(dic['data'])
    for i in range(count):
        FileHelper.save2File(content= 'Rank.%s %s VV : %s \n' % (i+1,dic['data'][i]['album_name'],dic['data'][i][key]), fileName=resultFileName,type= FileHelper.TYPE_APPEND)

    content.close()
    FileHelper.delFile(fileName)

def getsohuRank():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for keyWord in urls.keys():
        getData(keyWord=keyWord,type=TYPE_DAILY)
        time.sleep(1)
        getData(keyWord=keyWord,type=TYPE_WEEKLY)
        time.sleep(1)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for keyWord in urls.keys():
        getData(keyWord=keyWord,type=TYPE_DAILY)
        time.sleep(1)
        getData(keyWord=keyWord,type=TYPE_WEEKLY)
        time.sleep(1)
        #getData(keyWord=keyWord,type=TYPE_WEEKLY)
        #time.sleep(1)