#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

def timer(func): #time(test1)  func=test1
    def deco(*args,**kwargs):
        start_time = time.time()
        func(*args,**kwargs) # test1()
        stop_time = time.time()
        print('the func time is %s' % (stop_time - start_time))
    return deco
@timer  #test1 = timer(test1)
def test1():
    time.sleep(1)
    print('in the test1')

@timer  #test2 = timer(test2) = deco
def test2(name):
    time.sleep(1)
    print('in the test2',name)

test1()
test2("guo")
