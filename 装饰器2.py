#!/usr/bin/env python
# -*- coding:utf-8 -*-

user,passwd = 'guo','123'

def auth(auth_type):
    print("auth func:",auth_type)
    def outer_wrapper(func):
        def wrapper(*args,**kwargs):
            if auth_type == "local":
                username = input('Username: ').strip()
                password = input('Password: ').strip()
                if user == username and passwd == password:
                    print("User has passwd authentication")
                    re = func(*args,**kwargs)
                    print(re)
                else:
                    exit("Invalid username or password")
            if auth_type == "ldap":
                print("I'm ldap")
                func(*args, **kwargs)
        return wrapper
    return outer_wrapper

def index():
    print('welcome to index page')
@auth(auth_type="local")
def home():
    print('welcome to home page')
    return "from home"
@auth(auth_type="ldap")
def bbs():
    print('welcome to bbs page')

index()
home()
bbs()