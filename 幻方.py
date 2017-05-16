# -*- coding:utf-8 -*-

from numpy import *

def oddMagic(n):
    # 罗伯特法求奇数阶幻方/楼梯法
    A = zeros([n,n])
    posX = 0
    posY = int(n/2)
    for val in range(1,n**2+1):
        if int(A[posX,posY]):
            posX = mod(posX+2,n)
            posY = mod(posY-1,n)
        # 赋值并更新位置
        A[posX,posY] = int(val)
        posX = mod(posX-1,n)
        posY = mod(posY+1,n)
    return A

def magic(n):
    if mod(n,2):
        # 奇数阶
        A = oddMagic(n)
    elif mod( int(n/2) ,2 ):
        # 仅能被2整除，可拆分成四个奇数阶幻方
        a = int(n/2)
        A = zeros([n,n])
        A[:a,:a] = oddMagic(a)
        A[a:,a:] = oddMagic(a) + a**2
        A[:a,a:] = oddMagic(a) + 2*a**2
        A[a:,:a] = oddMagic(a) + 3*a**2
    else:
        # 仅能被4整除
        A = mat([i for i in range(1,n**2+1)]).reshape([n,n])
        J = mod( array([i for i in range(1,n+1)]) ,4 )>1.2
        for x in range(0,n):
            for y in range(0,n):
                if (J[x] == J[y]):
                    A[x,y] = n**2+1 - A[x,y]
    print(A)


magic(6)


-----------------------------------------------------------------------

# -*- coding: utf-8 -*-
# 奇阶幻方
def odd_magic_square(n):
    matrix = [[0 for i in range(n)] for i in range(n)]
    # x, y 的初始位置以及从1开始赋值
    num, x, y = 1, 0, int(n / 2)
    while num != n ** 2 + 1:
        matrix[x][y] = num
        # 通过x0,y0检测右上方是否已填入数字
        x0, y0 = x - 1, y + 1
        # 超界处理
        if x0 < 0:
            x0 += n
        if y0 == n:
            y0 = n - y0
        if matrix[x0][y0] == 0:
            x, y = x0, y0
        else:
            # 若有数字填入之前数字的下方
            x += 1
            if x == n:
                x = x - n
        num += 1
    i = 0
    while i < n:
        print(matrix[i], )
        i += 1


# 双偶幻方
def double_even_magic_square(n):
    num = 1
    matrix = [[] for i in range(n)]
    # 从1到n**2依次赋值
    for i in range(n):
        for j in range(n):
            matrix[i].append(num)
            num += 1
    # 小正方形的对角线上的数字取其补数
    for i in range(n):
        for j in range(n):
            if i % 4 == 0 and abs(i - j) % 4 == 0:
                for k in range(4):
                    matrix[i + k][j + k] = n ** 2 - matrix[i + k][j + k] + 1
            elif i % 4 == 3 and (i + j) % 4 == 3:
                for k in range(4):
                    matrix[i - k][j + k] = n ** 2 - matrix[i - k][j + k] + 1
    i = 0
    while i < n:
        print(matrix[i], )
        i += 1


odd_magic_square(3)
double_even_magic_square(4)
