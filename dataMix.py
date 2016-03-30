#!/usr/bin/python
# -*- coding: utf-8 -*-
# author zeck.tang
import json
import os

#从结果提取所需数据汇总
"""
从percent.txt : 移动端PC占比  p:PC  m:mobile
"""
def mixData(videoid = ''):
    if videoid == '' :
        print 'params lost'
    else :
        percentFile = open('percent.txt', 'r')
        infofileName = 'info.txt'
        percentfileName = 'percent.txt'
        infoFile = open(name='info.txt', mode='rw')
        result = open('result.txt', 'a')
        #print infoFile.read()
        percentDic = json.loads(percentFile.read().decode("utf-8"))
        infoDic = json.loads(infoFile.read().decode("utf-8"))
        print infoDic
        result.write(('name : %s ,' % infoDic['data']['name']).encode('utf-8'))
        result.write('videoid : %s ,' % videoid)
        #result.write(('description : %s \n' % infoDic['data']['description']).encode('utf-8'))
        result.write('url : %s ,' % infoDic['data']['url'])
        result.write('playCount : %s ,' % infoDic['data']['playCount'])
        result.write('albumId : %s ,' % infoDic['data']['albumId'])
        #result.write('videoType : %s \n' % infoDic['data']['videoType'])


        #result.write('url : %s \n' % url)
        #result.write('count : %s \n' % countDic[videoid])
        result.write('pc : %.0f %% ,' % percentDic['data']['p'])
        result.write('mobile : %.0f %% \n' % percentDic['data']['m'])

        print 'mixData over videoId :%s' % videoid

        infoFile.close()
        percentFile.close()
        result.close()
        if os.path.exists(infofileName):
            os.remove(infofileName)
            print'file %s removed' % (infofileName)
        else :
            print'file %s is not exist' % (infofileName)
        if os.path.exists(percentfileName):
            os.remove(percentfileName)
            print'file %s removed' % (percentfileName)
        else :
            print'file %s is not exist' % (percentfileName)
