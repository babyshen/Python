# 实现多线程简易ftp
#目前支持下载(get)和上传(put)(下载和上传支持md5校验)
#       列出服务端目录文件(ls)和列出本地目录文件(lls)
#       查看本地当前所在目录(lpwd)和服务端当前所在目录(pwd)
#       支持本地切换目录(lchdir)和服务端切换目录(chdir)
#（暂不支持创建文件和目录，对于权限等问题处理有待改善）
#

# ftp_server_start

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socketserver,json,os,hashlib,sys

class MyTCPHandler(socketserver.BaseRequestHandler):

    def put(self,*args):
        '''接受客户端文件'''
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        filesize = cmd_dic["size"]
        if os.path.isfile(filename):
            f = open(filename+".new",'wb')
        else:
            f = open(filename, 'wb')
        m = hashlib.md5()
        self.request.send(b'200 ok')
        received_size = 0
        while received_size < filesize :
            if filesize - received_size > 1024: #  要收不止一次,
                size = 1024
            else: # 最后一次，剩多少收多少
                size = filesize - received_size
            data = self.request.recv(size)
            m.update(data)
            f.write(data)
            received_size += len(data)
        else:
            print("file [%s] has uploaded" % filename)
        f.close()
        new_file_md5 = m.hexdigest()
        client_file_md5 = self.request.recv(1024)
        print("client file md5:", client_file_md5.decode())
        print("server file md5:", new_file_md5)

    def get(self, *args):
        cmd_dic = args[0]
        filename = cmd_dic["filename"]
        if os.path.isfile(filename):
            filesize = os.stat(filename).st_size
            print(filename)
            self.request.send(str(filesize).encode("utf-8"))# send file size
            f = open(filename,'rb')
            m = hashlib.md5()
            for line in f:
                m.update(line)
                self.request.send(line)
            print("file md5", m.hexdigest())
            f.close()
            self.request.send(m.hexdigest().encode("utf-8"))  # send md5
            print("send done...")
        else:
            self.request.send("not_exist".encode("utf-8"))

    def list(self,cmd_res):
        self.request.send(str(len(cmd_res)).encode("utf-8")) # 先发大小给客户端
        server_response = self.request.recv(1024)
        self.request.send(str(cmd_res).encode("utf-8"))

    def ls(self,*args):
        cmd_dic = args[0]
        dir_file = cmd_dic["filename"]
        if not dir_file:
            cmd_res = os.listdir()
            getattr(self, "list")(cmd_res)
        else:
            if os.path.isdir(dir_file):
                cmd_res = os.listdir(dir_file)
                getattr(self, "list")(cmd_res)
            else:
                cmd_res = "ls has no output"
                getattr(self,"list")(cmd_res)

    def pwd(self,*args):
        cmd_dic = args[0]
        cmd_res = os.getcwd()
        self.request.send(cmd_res.encode("utf-8"))

    def chdir(self,*args):
        cmd_dic = args[0]
        dirname = cmd_dic["dirname"]
        os.chdir(dirname)
        self.request.send(os.getcwd().encode("utf-8"))

    def handle(self):
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                print("{} wrote:".format(self.client_address[0]))
               # print(self.data)
                cmd_dic = json.loads(self.data.decode())
                action = cmd_dic["action"]
                if hasattr(self,action):
                    func = getattr(self,action)
                    func(cmd_dic)
            except ConnectionResetError as e:
                print("err,",e)
                break

if __name__ == "__main__":
    try:
        HOST, PORT = "0.0.0.0", 9999
        server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()
    except KeyboardInterrupt as e:
        sys.exit("")

# ftp_server_end

========================================分割线========================================

# ftp_client_start

#!/usr/bin/env python
# -*- coding:utf-8 -*-


import socket, os, json, hashlib, sys


class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()

    def help(self):
        msg = '''
        ls  # list server file
        lls # list client file
        gwd
        lgwd
        chdir dirname
        lchdir dirname
        get filename
        put filename
        '''
        print(msg)

    def connect(self, ip, port, *args, **kwargs):
        self.client.connect((ip, port))

    def interactive(self):
        while True:
            cmd = input(">>: ").strip()
            if not cmd: continue
            cmd_str = cmd.split()[0]
            if hasattr(self, "cmd_%s" % cmd_str):
                func = getattr(self, "cmd_%s" % cmd_str)
                func(cmd)
            else:
                self.help()

    def cmd_put(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                msg_dic = {
                    "action": "put",
                    "filename": filename,
                    "size": filesize,
                    #   "overridden":True
                }
                self.client.send(json.dumps(msg_dic).encode("utf-8"))
                #  防止粘包，等待服务器确认
                server_response = self.client.recv(1024)
                f = open(filename, 'rb')
                m = hashlib.md5()
                for line in f:
                    m.update(line)
                    self.client.send(line)
                else:
                    print("file upload success...")
                    f.close()
                print("file md5", m.hexdigest())
                self.client.send(m.hexdigest().encode("utf-8"))
            else:
                print(filename, "is not exist")

    def cmd_get(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
        msg_dic = {
            "action": "get",
            "filename": filename,
            # "size": filesize,
            # "overridden": True
        }
        self.client.send(json.dumps(msg_dic).encode("utf-8"))
        #  防止粘包，等待服务器确认
        server_response = self.client.recv(1024)
        if server_response.decode() != "not_exist":
            file_total_size = int(server_response.decode())
            received_size = 0
            if os.path.isfile(filename):
                f = open(filename+".new",'wb')
            else:
                f = open(filename, 'wb')
            m = hashlib.md5()
            while received_size < file_total_size:
                if file_total_size - received_size > 1024:  # 要收不止一次
                    size = 1024
                else:  # 最后一次，剩多少收多少
                    size = file_total_size - received_size
                data = self.client.recv(size)
                received_size += len(data)
                m.update(data)
                f.write(data)
                # print(file_total_size,received_size)
            else:
                new_file_md5 = m.hexdigest()
                print("file recv done...")
            f.close()
            server_file_md5 = self.client.recv(1024)
            print("server file md5:", server_file_md5.decode())
            print("client file md5:", new_file_md5)
        else:
            print(filename, "is not exist")

    def cmd_ls(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            dire_file = cmd_split[1]
        else:
            dire_file = ""
        msg_dic = {
            "action": "ls",
            "filename": dire_file,
        }
        self.client.send(json.dumps(msg_dic).encode("utf-8"))
        cmd_res_size = self.client.recv(1024)
        self.client.send(b"yes")
        received_size = 0
        received_data = b''
        while received_size < int(cmd_res_size.decode()):  # 判断接收长度，直到接收完毕
            data = self.client.recv(1024)
            received_size += len(data)
            received_data += data
        else:
            for file in received_data.decode().lstrip('[').rstrip(']').split(','):
                print(file)
            print("ls receive done..")

    def cmd_lls(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) == 1:
            cmd_res = os.listdir()
            for file in cmd_res:
                print(file)
        elif len(cmd_split)  > 1 :
            dir_file = cmd_split[1]
            if os.path.isdir(dir_file):
                cmd_res = os.listdir(dir_file)
                for file in cmd_res:
                    print(file)
            else:
                print(" %s : No such directory" % dir_file)

    def cmd_pwd(self,*args):
        cmd_split = args[0].split()
        if len(cmd_split) == 1:
            msg_dic = {
                "action": "pwd",
            }
            self.client.send(json.dumps(msg_dic).encode("utf-8"))
            cmd_res = self.client.recv(1024)
            print(cmd_res.decode())

    def cmd_lpwd(self,*args):
        cmd_split = args[0].split()
        if len(cmd_split) == 1:
            cmd_res = os.getcwd()
            print(cmd_res)

    def cmd_chdir(self,*args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            dirname = cmd_split[1]
            msg_dic = {
                "action": "chdir",
                "dirname":dirname
            }
            self.client.send(json.dumps(msg_dic).encode("utf-8"))
            cmd_res = self.client.recv(1024)
            print(cmd_res.decode())
        else:
            self.help()

    def cmd_lchdir(self,*args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            dirname = cmd_split[1]
            os.chdir(dirname)
            print(os.getcwd())
        else:
            self.help()

if __name__ == "__main__":
    try:
        ftp = FtpClient()
        ftp.connect('localhost', 9999)
        ftp.interactive()
    except ConnectionRefusedError  as e:
        sys.exit("Connection refused!")
    except KeyboardInterrupt as e:
        sys.exit("")

#ftp_client_end
