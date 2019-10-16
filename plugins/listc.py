#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import time
import re

class Source (object) :

    def __init__ (self):
        self.T = tools.Tools()
        self.now = int(time.time() * 1000)

    def getSource (self) :
        urlList = []

        # url = 'https://raw.githubusercontent.com/iptv-org/iptv/master/index.content.m3u'
        # req = [
        #     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        # ]
        # res = self.T.getPage(url, req)
        # if res['code'] == 200 :
            # print(res['body'])
            # body = res['body']
        fo = open("listc.m3u8", "r+")
        body = fo.read()
        # 关闭打开的文件
        fo.close()
        # print(body)
        pattern = re.compile(r"(?<=\",)(.*?)\n(.*?)\n", re.I|re.S)

        sourceList = pattern.findall(body)

        i = 1
        total = len(sourceList)
        for item in sourceList :
            info = self.T.fmtTitle(item[0])
            print('Checking[ %s / %s ]: %s' % (i, total, str(info['id']) + str(info['title'])))

            i = i + 1
            netstat = self.T.chkPlayable(item[1])

            if netstat > 0 :
                cros = 1 if self.T.chkCros(item[1]) else 0
                data = {
                    'title'  : str(info['id']) if info['id'] != '' else str(info['title']),
                    'url'    : str(item[1]),
                    'quality': str(info['quality']),
                    'delay'  : netstat,
                    'level'  : str(info['level']),
                    'cros'   : cros,
                    'online' : 1,
                    'udTime' : self.now,
                }
                urlList.append(data)
            else :
                pass # MAYBE later :P
        # else :
        #     pass # MAYBE later :P

        return urlList
