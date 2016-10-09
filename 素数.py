#!/usr/bin/env python
# -*- coding:utf-8 -*-

#方法一：
def prime_number(num):
    res = True
    if num <= 1:
        res = False
        return res
    for x in range(2,num-1):
        if num%x==0:
            res = False
            return res
        return res

print([x for x in range(100) if prime_number(x)])

#方法二：
def getPrime(maxNum):
    aList = [x for x in range(0, maxNum)]
    prime = []
    for i in range(2, len(aList)):
        if aList[i] != 0:
            prime.append(aList[i])
            clear(aList[i], aList, maxNum)
    return prime

def clear(aPrime, aList, maxNum):
    for i in range(2, int((maxNum / aPrime) + 1)):
        if not aPrime * i > maxNum - 1:
            aList[i * aPrime] = 0

print(getPrime(100))
