#!/usr/bin/env python  
#coding: utf-8  
import sys, os  
  
'''将当前进程fork为一个守护进程  
   注意：如果你的守护进程是由inetd启动的，不要这样做！inetd完成了  
   所有需要做的事情，包括重定向标准文件描述符，需要做的事情只有chdir()和umask()了  
'''  
  
def daemon (stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):  
     #重定向标准文件描述符（默认情况下定向到/dev/null）  
    try:   
        pid = os.fork()   
          #父进程(会话组头领进程)退出，这意味着一个非会话组头领进程永远不能重新获得控制终端。  
        if pid > 0:  
            sys.exit(0)   #父进程退出  
    except OSError, e:   
        sys.stderr.write ("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror) )  
        sys.exit(1)  
  
     #从母体环境脱离  
    os.chdir("/")  #chdir确认进程不保持任何目录于使用状态，否则不能umount一个文件系统。也可以改变到对于守护程序运行重要的文件所在目录  
    os.umask(0)    #调用umask(0)以便拥有对于写的任何东西的完全控制，因为有时不知道继承了什么样的umask。  
    os.setsid()    #setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离。  
  
     #执行第二次fork  
    try:   
        pid = os.fork()   
        if pid > 0:  
            sys.exit(0)   #第二个父进程退出  
    except OSError, e:   
        sys.stderr.write ("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror) )  
        sys.exit(1)  
  
     #进程已经是守护进程了，重定向标准文件描述符  
  
    for f in sys.stdout, sys.stderr: f.flush()  
    si = open(stdin, 'r')  
    so = open(stdout, 'a+')  
    se = open(stderr, 'a+')  
    os.dup2(si.fileno(), sys.stdin.fileno())    #dup2函数原子化关闭和复制文件描述符  
    os.dup2(so.fileno(), sys.stdout.fileno())  
    os.dup2(se.fileno(), sys.stderr.fileno())  
  
#示例函数：每秒打印一个数字和时间戳  
def main():  
    import time  
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid())  
    sys.stdout.write('Daemon stdout output\n')  
    sys.stderr.write('Daemon stderr output\n')  
    c = 0  
    while True:  
        sys.stdout.write('%d: %s\n' %(c, time.ctime()))  
        sys.stdout.flush()  
        c = c+1  
        time.sleep(1)  
  
if __name__ == "__main__":  
      daemone('/dev/null','/tmp/daemon_stdout.log','/tmp/daemon_error.log')  
      main()  
      
# 可以通过命令ps -ef | grep daemon.py查看后台运行的继承
# 在/tmp/daemon_error.log会记录错误运行日志
# 在/tmp/daemon_stdout.log会记录标准输出日志。
