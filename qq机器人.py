#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 已加入天气预报，翻译，学习，后续会继续扩展添加
# qqbot 详细介绍 https://github.com/pandolia/qqbot/

import random
import hashlib
import requests
import qqbot
import json

file = 'qq.txt'

if os.path.exists(file):
    mess = json.load(open(file, 'r'))
else:
    with open(file,'w') as f:
        f.write('{}')
    mess = json.load(open(file, 'r'))


def weather(city):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-agent': user_agent}
    
    r = city
    url = 'http://www.sojson.com/open/api/weather/json.shtml?city=' + city
    
    html = requests.get(url,headers=headers)
    result = json.loads(html.text)
    if result.get('status') != 200:
        return "暂无【%s】天气预报！" % city
    res = result.get('data').get('forecast')
    for i in res:
        r += '\r\n' + i.get('date') + ' ' + i.get('type') + ' ' + i.get('low') + ' ' + i.get('high') + ' ' + i.get(
            'fengli') + ' ' + i.get('fengxiang')
    return r


def translate(word):
    appid = 'xxoo' # 去百度翻译api申请
    secretKey = 'ooxx' # 去百度翻译api申请

    myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    fromLang = 'auto'
    toLang = 'auto'
    salt = random.randint(32768, 65536)

    sign = appid + word + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode())
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + word + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    r = requests.get(myurl).text
    res = json.loads(r)
    return res.get('trans_result')[0].get('dst')


@qqbot.QQBotSlot
def onQQMessage(bot, contact, member, content):
    if "@ME" in content:
        con = '圈我干啥？？'
        bot.SendTo(contact, con)
    elif content.startswith("#study#") and '#get#' not in content and len(content.split()) >= 3:
        key, *value = content.split()[1:]
        mess[key] = value
        con = "录入成功！"
        json.dump(mess, open('qq.txt', 'w'))
        bot.SendTo(contact, con)
    elif content.startswith('#get#') and len(content.split()) >= 2:
        key = content.split()[1]
        con = mess.get(key) if key in mess else '不存在'
        bot.SendTo(contact, ' '.join(con))
    elif content.startswith("#weather#") and len(content.split()) >= 2:
        con = weather(content.split()[1])
        bot.SendTo(contact, con)
    elif content.startswith('#translate#') and len(content.split()) >= 2:
        word = ' '.join(content.split()[1:])
        con = translate(word)
        bot.SendTo(contact, con)
    elif content.startswith('#show#'):
        con = ""
        for i in mess:
            con += i + ':' + str(mess[i]) + '\r\n'
        bot.SendTo(contact, con)


if __name__ == '__main__':
    qqbot.RunBot()
