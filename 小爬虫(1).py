#!/usr/bin/env python
# 
import re
import urllib

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    reg = r'src="(.*?\.jpg)"'
    imgre = re.compile(reg)
    imglist = re.findall(imgre,html)
    x=0
    for imgurl in  imglist:
        urllib.urlretrieve(imgurl,'%s.jpg' % x)
        x+=1

html = getHtml("http://tieba.baidu.com/p/4616787813?da_from=ZGFfbGluZT1EVCZkYV9wYWdlPTEmZGFfbG9jYXRlPXAwMDY0JmRhX2xvY19wYXJhbT0zJmRhX3Rhc2s9dGJkYSZkYV9vYmpfaWQ9MjM3MDYmZGFfb2JqX2dvb2RfaWQ9NDM3ODYmZGFfdGltZT0xNDY3MzY3MDc2&da_sign=d5fe9344fcf9b795009e1fffc98e51db&tieba_from=tieba_da")
getImg(html)
