# 模拟nmap扫描端口

#!/usr/bin/env python
# -*- coding:utf-8 -*-

__version__ = '1.1.1'

import socket
import threading
import time
import argparse
import ipaddress

openPortNum = 0
socket.setdefaulttimeout(3)

def socket_port(ip, PORT):
    global openPortNum
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((ip, PORT))
    if(result == 0):
        print(ip, PORT,'is open')
        openPortNum += 1
        s.close()

def start_scan(IP):
    for port in range(0, 65535+1):
        threading.Thread(target=socket_port, args=(IP, int(port))).start()
        time.sleep(0.006)

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-V','--version', action='version', version='%(prog)s '+ __version__)
    parser.add_argument('ip',metavar="IP",nargs='+',help="IP Address")
    args = parser.parse_args()
    return args.ip

if __name__ == '__main__':
    args = args_parser()
    t = time.time()
    for i in args:
        try:
            ipaddress.ip_address(i)
            start_scan(i)
            print()
        except ValueError as e:
            print(e,'\n')

    print('total open port is %s, scan used time is: %f' %(openPortNum, time.time()-t))
