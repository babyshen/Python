#利用python批量修改SecureCRT会话密码
# -*- coding:utf-8 -*-
import os,re
 
def CRT_Path(path,*args,**kwargs):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            fullname = os.path.join(dirpath, file)
            f1 = open(fullname,'r',encoding="utf-8")
            alllines = f1.readlines()
            f1.close()
            f2 = open(fullname, 'w',encoding="utf-8")
            pw_r = re.compile(r'("Password V2"=)(.*)')
            if 'admin' in alllines[0]:  # 判断用户名是否是admin（可根据需要修改）
                for eachline in alllines:
                    a = re.sub(pw_r,'\g<1>'+admin_pwd,eachline)
                    f2.writelines(a)
            elif 'root' in alllines[0]: #判断用户名是否是root（可根据需要修改），有其他继续添加就行
                for eachline in alllines:
                    a = re.sub(pw_r,'\g<1>'+root_pwd,eachline)
                    f2.writelines(a)
            else:
                f2.writelines(alllines)
            f2.close()
 
if __name__ == '__main__':
    # admin 密码加密字符串
    admin_pwd = 'xxooxxoo'
    # root 密码加密字符串
    root_pwd = 'xxooxxooxxoo'
    path = r'C:\Users\root\Desktop\Sessions'  # CRT Seesions 路径
    CRT_Path(path)
