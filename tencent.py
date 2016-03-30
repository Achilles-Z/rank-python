#!/usr/bin/python
# -*- coding: utf-8 -*-
# author zeck.tang

import time
import datetime
import FileHelper
import sys

from bs4 import BeautifulSoup
# 视频基础信息 -不带VV
#http://data.video.qq.com/fcgi-bin/data?tid=205&appid=20001059&appkey=c8094537f5337021&otype=json&idlist=zf2z0xpqcculhcz&callback=jQuery111009964865940087164_1458888349737&low_login=1&_=1458888349738
#返回内容
"""
jQuery111009964865940087164_1458888349737({"costtime":117,"errormsg":"","errorno":0,"resptime":1458888350
,"results":[{"fields":{"director":["兹比格涅夫·布热津斯基","戴维·贝尼奥夫","D.B. Weiss"],"director_id":["500939","147138"
,"206311"],"director_info":[null,{"pic200x200":"http://i.gtimg.cn/qqlive/images/namelib/v688/1/3/8/147138
.jpg"},{"pic200x200":"http://i.gtimg.cn/qqlive/images/namelib/v688/3/1/1/206311.jpg"}],"douban_id":"3016187"
,"douban_score":"9.3","episode_all":"50","episode_publish":"","episode_updated":"全50集","keyword":["权
力的游戏","伊萨克·亨普斯特德-怀特","查尔斯·丹斯","艾米莉亚克拉克","罗恩·多纳基","伊恩·麦克尔希尼","肖恩"],"leading_actor":["伊萨克·亨普斯特德-怀特","查
里斯·丹斯","约翰·C·布莱德利","罗恩·多纳基","伊恩·麦克尔希尼","肖恩·宾","艾米莉亚·克拉克","基特·哈灵顿"],"leading_actor_id":["147140","75954"
,"154486","154487","71495","77848","147142","84085"],"leading_actor_info":[{"pic200x200":"http://i.gtimg
.cn/qqlive/images/namelib/v688/1/4/0/147140.jpg"},{"pic200x200":"http://i.gtimg.cn/qqlive/images/namelib
/v688/9/5/4/75954.jpg"},{"pic200x200":"http://i.gtimg.cn/qqlive/images/namelib/v688/4/8/6/154486.jpg"
},{"pic200x200":"http://i.gtimg.cn/qqlive/images/namelib/v688/4/8/7/154487.jpg"},{"pic200x200":"http
://i.gtimg.cn/qqlive/images/namelib/v688/4/9/5/71495.jpg"},{"pic200x200":"http://i.gtimg.cn/qqlive/images
/namelib/v688/8/4/8/77848.jpg"},{"pic200x200":"http://i.gtimg.cn/qqlive/images/namelib/v688/1/4/2/147142
.jpg"},{"pic200x200":"http://i.gtimg.cn/qqlive/images/namelib/v688/0/8/5/84085.jpg"}],"producer":null
,"singer_name":null},"id":"zf2z0xpqcculhcz","retcode":0}]})
"""

# 评论条数
# http://coral.qq.com/article/1150553426/commentnum?callback=jQuery111009964865940087164_1458888349737&low_login=1&_=1458888349756
# http://coral.qq.com/article/1150553426/commentnum?callback=jQuery111107618353636986395_1458888351797&_=1458888351798
# 返回内容
"""
jQuery111009964865940087164_1458888349737({"errCode":0,"data":{"targetid":1150553426,"commentnum":"8351"
},"info":{"time":1458888351}})
"""

# 热门评论
# http://coral.qq.com/article/1150553426/hotcomment?reqnum=10&callback=hotcommentList&_=1458888351799


# 播放VV allnumc=合集播放总量 allnumc_m=正片播放总量 tdnumc=今天合集播放量 tdnumc_m=今天正片播放量
# http://data.video.qq.com/fcgi-bin/data?tid=70&&appid=10001007&appkey=e075742beb866145&callback=jQuery19100054316992779228634_1458890862241&low_login=1&idlist=maljebn62xg27dc&otype=json&_=1458890862243
# idlist 合集id -- 可以从指数搜索的 url中获得 x2bk0683nkpiocd
# 返回内容
"""
jQuery19100054316992779228634_1458890862241({"costtime":91,"errormsg":"","errorno":0,"resptime":1458890882
,"results":[{"fields":{"allnumc":127163870,"allnumc_m":70353677,"c_column_id":0,"column":null,"tdnumc"
:45773,"tdnumc_m":42226},"id":"maljebn62xg27dc","retcode":0}]})
"""


#'http://v.qq.com/cover/'

urls = {
    '2':'drama',
    '1':'movie',
    '10':'show',
    '3':'comic'
}

TYPE_DAILY = 2
TYPE_WEEKLY = 3
TYPE_MONTHLY = 4
TYPE_TOTAL = 1

"""
拼接url
"""
def getUrl(channle = '',type =''):
    if channle == ''  or type == '':
        print 'params lost'
        return False
    else:
        return 'http://v.qq.com/rank/detail/%s_-1_-1_-1_%s_-1.html' % (channle,type)

def getData(keyWord = '',type = ''):
    targetUrl = getUrl(keyWord,type)
    todayTime = datetime.date.today()
    filePath = FileHelper.getPath(todayTime,'tencent',urls[keyWord])
    fileName = '%s/html.txt' % filePath
    FileHelper.getContent2FileWithoutProcess(fileName=fileName,targetUrl=targetUrl)
    content = open(fileName,'r')
    temp = content.read().decode('utf-8')
    soup = BeautifulSoup(temp,'html.parser')
    count = -1 #过滤第一个
    Rank = 0
    resultFileName=''
    if type == TYPE_DAILY:
        resultFileName='%s/RankDaily.txt' % filePath
    if type == TYPE_WEEKLY:
        resultFileName='%s/RankWeekly.txt' % filePath
    if type == TYPE_MONTHLY:
        resultFileName='%s/RankMonthly.txt' % filePath
    for tag in soup.findAll(True):
        if(tag.name == 'a' and tag.has_attr('href') and (''.join(tag['href']).find('cover') > 0)):
            Rank = Rank+1
            FileHelper.save2File(content = 'Rank.%s %s ' % (Rank,tag['title'] ), fileName=resultFileName,type= FileHelper.TYPE_APPEND)
        if (tag.has_attr('class') and tag.name == 'strong' and ''.join(tag['class']) == 'num'):
            FileHelper.save2File(content = 'VV : %s \n' % tag.string , fileName=resultFileName,type= FileHelper.TYPE_APPEND)

    content.close()
    FileHelper.delFile(fileName)

def gettencentRank():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for keyWord in urls.keys():
        getData(keyWord=keyWord,type=TYPE_DAILY)
        time.sleep(1)
        getData(keyWord=keyWord,type=TYPE_WEEKLY)
        time.sleep(1)
        getData(keyWord=keyWord,type=TYPE_MONTHLY)
        time.sleep(1)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    for keyWord in urls.keys():
        getData(keyWord=keyWord,type=TYPE_DAILY)
        time.sleep(1)
        getData(keyWord=keyWord,type=TYPE_WEEKLY)
        time.sleep(1)
        getData(keyWord=keyWord,type=TYPE_MONTHLY)
        time.sleep(1)