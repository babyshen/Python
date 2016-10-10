#!/usr/bin/env python
# -*- coding:utf-8 -*-

#方法一：
#这效率比较低，追求效率的话可以试试下一个方法
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
#如果要追求一下速度的话，可以试试这个(求1千万内素数14秒左右秒).
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

#方法三
def fun(max):
    l = []
    a = [x for x in range(max + 1)]
    for i in range(2, max):
        if a[i]:
            l.append(a[i])
            for j in range(2, int(max/a[i])+1):
                if j * a[i] <= max - 1:
                    a[a[i] * j] = 0
    print(l)

fun(10000000)

