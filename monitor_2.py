#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__  = 'babyshen'
__version__ = '1.0.0'
__datetime__ = '2016-12-30 03:30:00'

import os
import argparse
import time
import subprocess
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
from email import encoders

def daemon():
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        sys.exit(1)

    os.chdir('/')
    os.umask(0)
    os.setsid()

    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        sys.exit(1)

# server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject="", text="", files=[]):
    assert type(server) == dict
    assert type(to) == list
    assert type(files) == list

    msg = MIMEMultipart()
    msg['From'] = fro  # 邮件的发件人
    msg['Subject'] = subject  # 邮件的主题
    msg['To'] = COMMASPACE.join(to)  # COMMASPACE==', ' 收件人可以是多个，to是一个列表
    msg['Date'] = formatdate(localtime=True)  # 发送时间
    msg.attach(MIMEText(text, 'plain', 'utf-8'))

    for file in files:  # 添加附件可以是多个，files是一个列表，可以为空
        part = MIMEBase('application', 'octet-stream')  # 'octet-stream': binary data
        with open(file, 'rb') as f:
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    smtp = smtplib.SMTP()
    smtp.connect(server['name'])  # connect有两个参数，第一个为邮件服务器，第二个为端口，默认是25
    smtp.login(server['user'], server['passwd'])  # 用户名，密码
    smtp.sendmail(fro, to, msg.as_string())  # 发件人，收件人，发送信息
    smtp.close()  # 关闭连接


def ping_test(src, dest):
    ping = subprocess.Popen('/bin/ping -i 0.2 -c 4 -q -I ' + src + ' ' + dest,
                            shell=True,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)  # 执行命令
    res, err = ping.communicate()
    if err: sys.exit(res.decode().strip('\n'))
    pres = list(res.decode().split('\n'))
    loss = pres[3].split()[5]  # 获取丢包率
    try:
        rtt = pres[4].split('/')[4]  # 获取rtt avg值
    except IndexError:
        rtt = ""
    return loss, rtt

def ping_res(file,outfile):
    with open(file, 'r', encoding='utf-8') as f:
        with open(outfile, 'w', encoding='utf-8') as f1:
            textmail = text = 'host src dest loss rtt\n'
            f1.write(text)
            for line in f:
                host = line.split()[0]
                src = line.split()[1]
                dest = line.split()[2]
                threshold = line.split()[3] if len(line.split()) == 3 else 100
                loss, rtt = ping_test(src, dest)
                text = '%s %s %s %s %s \n' % (host, src, dest, loss, rtt)
                f1.write(text)
                if float(loss.strip('%')) > 10 or float(rtt) > float(threshold):
                    # text1 = 'host src dest loss rtt\n'
                    textmail += '%s %s %s %s %s \n' % (host, src, dest, loss, rtt)
    return textmail

def args_parser(file,outfile):
    description = """netmon"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-V', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-f','--file',default=file,dest='file',help="netmon file, default: "+file)
    parser.add_argument('-o','--outfile',default=outfile,dest='outfile',help="output file, default: "+outfile)
    parser.add_argument('-d','--daemon',action='store_const',const='daemon',help="daemon mode, fork into background")
    args = parser.parse_args()
    return args.file,args.outfile,args.daemon

if __name__ == '__main__':
    try:
        # file 配置文件，格式(空格隔开)：主机名，源地址，目标地址，延时阀值(默认是100)
        file = '/root/ping_test/ping_test.cfg'
        outfile = '/root/ping_test/ping_test.rev' # 结果文件
        file ,outfile,dflag = args_parser(file,outfile)
        if dflag : daemon() # 如果daemon flag为真，即有-d/--daemon参数，则运行daemon mode
        # print(file,outfile,dflag)
        server = {'name':'xxx',
                  'user':'ooo',
                  'passwd':''}
        fro = 'xxoo'
        to = ['ooxx']
        subject = 'ping_test'
        while True:
            textmail = ping_res(file, outfile)
            # print(textmail) # 可以用来输出邮件内容
            if len(textmail.split('\n')) == 2 : sys.exit() # 当只有一行时退出程序不发送邮件
            send_mail(server,fro,to,subject,textmail)
            time.sleep(300)
    except smtplib.SMTPAuthenticationError :
        sys.exit("Mail Authentication Failed")
    except KeyboardInterrupt :
        sys.exit(249)
    except Exception as e:
        sys.exit(e)
        
