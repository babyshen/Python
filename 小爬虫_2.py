# python 3.5    版本

#!/usr/bin/env python
# -*- coding:uft-8 -*-

import urllib.request
import re

def getHtml(url):
    page = urllib.request.urlopen(url)
    return page.read()

def getImg(html):
    imgre = re.compile(r'src="(.+?\.jpg)" pic_ext')
    imglist = re.findall(imgre,html)
    x = 0
    for imgurl in imglist:
        urllib.request.urlretrieve(imgurl,'%s.jpg' % x)
        x+=1

html = getHtml("http://tieba.baidu.com/p/2460150866")

getImg(html.decode())
