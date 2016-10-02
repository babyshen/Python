#!/usr/bin/env python
# -*- coding:utf-8 -*-

c = 0
for i in range(1,10):
    for a in range(1,i+1):
        c = i * a
        print("%s * %s = %s" %(a,i,c),end="\t")
    print()
