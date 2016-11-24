# -*- coding:utf-8 -*-

# IP地址十六进制二进制间相互转换
 
import ipaddress,sys

def ip2hex_bin(file,*args,**kwargs):
    try:
        with open(file,'r',encoding='utf-8') as f:
            allip = f.readlines()
        ip = [ ipaddress.IPv4Address(ip.strip('\n')) for ip in allip ]
        if flag == '-h':
            for i in ip:
                print(hex(int(i)))
        else:
            for i in ip:
                print(bin(int(i)))
    except Exception as e:
        print(e)

def hex_bin2ip(file,*args,**kwargs):
    try:
        with open(file,'r',encoding='utf-8') as f:
            allip = f.readlines()
        for i in allip:
            a = i.strip('\n')
            print(ipaddress.IPv4Address(int(a,0)))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    try:
        flag = sys.argv[1]
        file = sys.argv[2]
        IP = {
            '-b':ip2hex_bin,
            '-h':ip2hex_bin,
            '-i':hex_bin2ip
        }
        IP.get(flag)(file)
    except Exception as e:
        print(sys.argv[0],'[-b|-h|-i] file')
 
