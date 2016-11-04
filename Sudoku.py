#核心算法：随机填充9x9长度的一维数组，用算法模拟出二维矩阵。填充函数以行为单位，但每一次填充格子前都先计算当前格子的可能数
#如果可能数为零则重置当前行所有数据，重新填充
#如果当前行连续随机填充了10次都无法完成，则回退到初始化函数并返回false，回退到上一行填充

#!/usr/bin/env python

import random
import time
MAX_ROW_RETRY = 10
MAX_RETRY=100
def initEmptyList():
    #初始化一个全0的空数组
    mlist = []
    for i in range (0,81):
        mlist.append(0)
    return mlist

def x(index):
    #根据当前格子编号获取其所在行
    x = index%9
    if(x==0):
        x=9
    return x

def y(index):
    #根据当前格子编号获取其所在列
    y = (index-1)//9+1
    if(y>9):
        y = 9
    return y

def getRowByIndex(mlist,index):
    #根据当前格子编号获取其所在行的全部数字
    startindex = (index-1)//9*9+1
    return mlist[startindex-1:startindex+8]

def getColumnByIndex(mlist,index):
    #根据当前格子编号获取其所在列的全部数字
    col = []
    colindex = x(index)
    for i in range (0,9):
        col.append(mlist[i*9+colindex-1])
    return col

def getAreaByIndex(mlist,index):
    #根据当前格子编号获取其所在区域的全部数字
    area = []
    startcol = (x(index)-1)//3*3+1
    #计算index所在区域的起始列
    startrow = (y(index)-1)//3*3+1
    #计算index所在区域的起始行
    for i in range (0,3):
        startindex = (startrow+i-1)*9+startcol
        #计算本区域在一维数组中的起始坐标
        area.extend(mlist[startindex-1:startindex+2])
    return area

def isPossible(mlist,index):
    possibility = [1,2,3,4,5,6,7,8,9]
    for v in range(1,10):
        if(getRowByIndex(mlist,index).count(v)!=0):
            possibility.remove(v)
            #发现同一行已经存在这数字，则从可能列表中移除该数字
        elif(getColumnByIndex(mlist,index).count(v)!=0):
            possibility.remove(v)
            #发现同一列已经存在这数字，则从可能列表中移除该数字
        elif(getAreaByIndex(mlist,index).count(v)!=0):
            possibility.remove(v)
            #发现同一区域已经存在这数字，则从可能列表中移除该数字
    return possibility

def initSudoku():
    row = 1
    #行指针
    row_retry = 0
    #行填充重试计数器
    retry=0
    #总重试计数器
    finish = False
    #"等Finish是True了我就回老家结婚"
    mlist = initEmptyList()
    #存放数字的数组
    while(not finish):
        row_finish = fillRowBlocks(mlist,row)
        #尝试填充
        if(row_finish):
            if(row==9):
                #如果全部搞定，直接返回
                return mlist
            else:
                #只是搞定了一行，进入下一行
                row+=1
        else:
            if(row_retry==MAX_ROW_RETRY):
                row-=1
                row_retry=0
                retry+=1
                #如果达到行填充最大重试次数，则回退一行（这他妈就是回溯！我昨天想了一下没想明白！）
            else:
                row_retry+=1
                #如果没有达到最大，继续尝试
        if(retry==MAX_RETRY):
            mlist = initEmptyList()
            row = 1
            row_retry = 0
            retry = 0
            #如果达到全局最大尝试次数，清零数组重新开始
    #没错，这里根本不需要是否退出总循环的Flag，完成这个只是时间问题
    return ['Unknown Error']

def fillRowBlocks(mlist,row):
    result = False
    for i in range((row-1)*9,row*9):
        mlist[i]=0
    #重置该行数据
    for i in range (0,9):
        for j in range((row - 1) * 9, row * 9):
            plist = isPossible(mlist,j+1)
            plen = len(plist)
            #判断当前格子可以填入的数字有几个
            if(len(plist)!=0):
                k = plist[random.randint(0, plen-1)]
                mlist[j]=k
                result = True
                #如果可以填入数字则填入，并设flag为真
            else:
                result = False
                break
                #如果发现无法填入数字，中断本次尝试并设flag为假
        if(result==True):
            break
            #如果flag为真，就没有必要继续其他尝试了，因为最后一个格子的填充结果一定是最终的Flag结果
    return result

def printSudoku(mlist):
    for i in range (0,9):
        print(mlist[i*9:i*9+9])
    print('===========================')

totaltime = 0
for i in range (1,3): # 循环次数，输出几次数独
    start = time.clock()
    sudoku = initSudoku()
    end = time.clock()
    curtime = end-start
    totaltime += curtime
    printSudoku(sudoku)
    print('本次时间 %.4f 秒, 平均时间 %.4f 秒' % (curtime,totaltime/i))
    time.sleep(0.1)
