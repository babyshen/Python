# -*- coding:utf-8 -*-
# 可以查询天气预报，进行学习录入

import requests
import qqbot
import json

mess = json.load(open('qq.txt', 'r'))


def weather(city):
    r = ""
    url = 'http://www.sojson.com/open/api/weather/json.shtml?city=' + city
    html = requests.get(url)
    result = json.loads(html.text)
    if result.get('status') != 200:
        return "暂无【%s】天气预报！" %city
    res = result.get('data').get('forecast')
    for i in res:
        r += '\r\n' + i.get('date') + ' ' + i.get('type') + ' ' + i.get('low') + ' ' + i.get('high') + ' ' + i.get(
            'fengli') + ' ' + i.get('fengxiang')
    return r


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


if __name__ == '__main__':
    qqbot.RunBot()
