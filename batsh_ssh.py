# 多台设备批量执行ssh命令

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import paramiko

class SSh(object):
    def __init__(self,port,username,password):
        self.port = port
        self.username = username
        self.password = password

    def ssh_con(self,host,ip,cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip,self.port,self.username,self.password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        res,err = stdout.read(),stderr.read()
        result = res if res else err
        print('\033[31;1m%s %s\033[0m' %(host,ip))
        print('\033[32;1m%s\033[0m' %result.decode())
        ssh.close()

if __name__ == '__main__':
    client   = {'host1':'1.1.1.1',
                'host2':'2.2.2.2',
                'host3':'3.3.3.3',
                'host4':'4.4.4.4',
              }               # 主机列表 ，hostname:ip
    port     = 22             # 端口号
    username = 'root'         # 用户名
    password = '123456789'    # 密码
    
    cmd = "ip route show match 1.1.1.1 | head -1" # 要执行的命令
    
    ssh = SSh(port,username,password)
    for i in client:
        host,ip = i,client[i]
        try:
            ssh.ssh_con(host,ip,cmd)
        except WindowsError:
            print('\033[31;1m%s %s %s \033[0m\n' %(host,ip,'连接尝试失败'))
        except Exception as e:
            print(e)
