#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''批量修改SecureCRT密码'''
import os,re

def CRT_Path(path,*args,**kwargs):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            fullname = os.path.join(dirpath, file)
            f1 = open(fullname,'r',encoding="utf-8")
            alllines = f1.readlines()
            f1.close()
            f2 = open(fullname, 'w',encoding="utf-8")
            if 'babyshen' in alllines[0]:  # 判断用户名是否是babyshen（可根据需要修改）
                for eachline in alllines:
                    a = re.sub(r'("Password V2"=)(.*)','\g<1>加密字符串',eachline)
                    f2.writelines(a)
            elif 'root' in alllines[0]: #判断用户名是否是root（可根据需要修改），有其他继续添加就行
                for eachline in alllines:
                    a = re.sub(r'("Password V2"=)(.*)','\g<1>加密字符串',eachline)
                    f2.writelines(a)
            else:
                f2.writelines(alllines)
            f2.close()

if __name__ == '__main__':
    path = 'C:\program1\CRT\conf\Sessions\VMware'  # Seesions 路径
    CRT_Path(path)
    
