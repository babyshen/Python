#!/usr/bin/env python
# -*- coding:utf-8 -*-

def Verification_Code():
    '''
    Verification code module, including the size of the letters and numbers, a total of four.
    :return:
    '''
    import random
    checkcode = ''
    for i in range(4):
        current = random.randrange(0, 4)
        if current > i:
            temp = chr(random.randint(65, 90))
        elif current < i:
            temp = chr(random.randint(97, 122))
        else:
            temp = random.randint(0, 9)
        checkcode += str(temp)
    return checkcode

if __name__ == "__main__":
    Verification_Code()
