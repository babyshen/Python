# 解数独
#coding:utf-8
#python2.7

import numpy as np
from Queue import Queue, LifoQueue
import time
import copy

class Recoder():
    point = None        #进行猜测的点
    point_index = 0     #猜测候选列表使用的值的索引
    value = None        #回溯记录的值

class Sudo():
    def __init__(self, data):
        #数据初始化(二维的object数组)
        self.value = np.array([[0]*9]*9, dtype=object)
        self.new_points = Queue()  #先进先出的新解坐标
        self.recoder = LifoQueue() #先进后出的回溯器
        self.guess_times = 0       #猜测次数

        #九宫格的基准列表
        self.base_points=[[0,0],[0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]

        #整理数据
        data = np.array(data).reshape(9,-1)
        for r in range(0,9):
            for c in range(0,9):
                if data[r,c]:
                    self.value[r,c] = data[r,c]
                    #新点添加到列表中，以便遍历
                    self.new_points.put((r,c))
                else:
                    self.value[r,c] = [1,2,3,4,5,6,7,8,9]

    #剔除数字
    def _cut_num(self, point):
        r, c = point
        val = self.value[r, c]

        #行
        for i, item in enumerate(self.value[r]):
            if isinstance(item, list):
                if item.count(val):
                    item.remove(val)

                    #判断移除后，是否剩下一个元素
                    if len(item)==1:
                        self.new_points.put((r, i))
                        self.value[r,i] = item[0]

        #列
        for i, item in enumerate(self.value[:,c]):
            if isinstance(item, list):
                if item.count(val):
                    item.remove(val)

                    #判断移除后，是否剩下一个元素
                    if len(item)==1:
                        self.new_points.put((i, c))
                        self.value[i,c] = item[0]

        #所在九宫格(3x3的数组)
        b_r, b_c = map(lambda x:x/3*3, point) #九宫格基准点
        for m_r, row in enumerate(self.value[b_r:b_r+3, b_c:b_c+3]):
            for m_c, item in enumerate(row):
                if isinstance(item, list):
                    if item.count(val):
                        item.remove(val)

                        #判断移除后，是否剩下一个元素
                        if len(item)==1:
                            r = b_r + m_r
                            c = b_c + m_c
                            self.new_points.put((r, c))
                            self.value[r,c]=item[0]

    #同一行、列或九宫格中1~9可能性只有一个的情况
    def _check_one_possbile(self):
        #同一行只有一个数字的情况
        for r in range(0,9):
            values = filter(lambda x:isinstance(x,list), self.value[r])

            for c, item in enumerate(self.value[r]):
                if isinstance(item, list):
                    for value in item:
                        if sum(map(lambda x:x.count(value), values)) == 1:
                            self.value[r,c] = value
                            self.new_points.put((r,c))
                            return True

        #同一列只有一个数字的情况
        for c in range(0,9):
            values = filter(lambda x:isinstance(x,list), self.value[:,c])

            for r, item in enumerate(self.value[:,c]):
                if isinstance(item, list):
                    for value in item:
                        if sum(map(lambda x:x.count(value), values)) == 1:
                            self.value[r,c] = value
                            self.new_points.put((r,c))
                            return True

        #九宫格内的单元格只有一个数字的情况
        for r,c in self.base_points:
            values = filter(lambda x:isinstance(x,list), self.value[r:r+3,c:c+3].reshape(1,-1)[0])

            for m_r, row in enumerate(self.value[r:r+3,c:c+3]):
                for m_c, item in enumerate(row):
                    if isinstance(item, list):            
                        for value in item:
                            if sum(map(lambda x:x.count(value), values)) == 1:
                                self.value[r+m_r, c+m_c] = value
                                self.new_points.put((r+m_r, c+m_c))
                                return True

    #同一个九宫格内数字在同一行或同一列处理
    def _check_same_num(self):
        for b_r, b_c in self.base_points:
            block = self.value[b_r:b_r+3,b_c:b_c+3]

            #判断数字1~9在该九宫格的分布情况
            data = block.reshape(1,-1)[0]
            for i in range(1,10):
                result = map(lambda x: 0 if not isinstance(x[1], list) else x[0]+1 if x[1].count(i) else 0, enumerate(data))
                result = filter(lambda x:x>0,result)
                r_count = len(result)
 
                if r_count in [2, 3]:
                    #2或3个元素才有可能同一行或同一列
                    rows = map(lambda x:(x-1)/3, result)
                    cols = map(lambda x:(x-1)%3, result)

                    if len(set(rows)) == 1:
                        #同一行，去掉其他行的数字
                        result = map(lambda x: b_c + (x-1)%3, result)
                        row = b_r + rows[0]

                        for col in range(0,9):
                            if not col in result:
                                item = self.value[row, col]
                                if isinstance(item, list):
                                    if item.count(i):
                                        item.remove(i)

                                        #判断移除后，是否剩下一个元素
                                        if len(item)==1:
                                            self.new_points.put((row, col))
                                            self.value[row, col] = item[0]
                                            return True
                        
                    elif len(set(cols)) == 1:
                        #同一列
                        result = map(lambda x: b_r + (x-1)/3, result)
                        col = b_c + cols[0]
 
                        for row in range(0,9):
                            if not row in result:
                                item = self.value[row, col]
                                if isinstance(item, list):
                                    if item.count(i):
                                        item.remove(i)

                                        #判断移除后，是否剩下一个元素
                                        if len(item)==1:
                                            self.new_points.put((row, col))
                                            self.value[row, col] = item[0]
                                            return True

    #排除法解题
    def solve_sudo(self):
        is_run_same = True
        is_run_one = True

        while is_run_same:
            while is_run_one:
                #剔除数字
                while not self.new_points.empty():
                    point = self.new_points.get() #先进先出
                    self._cut_num(point)

                #检查单个数字的情况
                is_run_one = self._check_one_possbile()

            #检查同行或列的情况
            is_run_same = self._check_same_num()
            is_run_one = True

    #得到有多少个确定的数字
    def get_num_count(self):
        return sum(map(lambda x: 1 if isinstance(x,int) else 0, self.value.reshape(1,-1)[0]))

    #评分，找到最佳的猜测坐标
    def get_best_point(self):
        best_score = 0
        best_point = (0,0)

        for r, row in enumerate(self.value):
            for c, item in enumerate(row):
                point_score = self._get_point_score((r,c))
                if best_score < point_score:
                    best_score = point_score
                    best_point = (r,c)
        return best_point

    #计算某坐标的评分
    def _get_point_score(self, point):
        #评分标准 (10-候选个数) + 同行确定数字个数 + 同列确实数字个数
        r,c = point
        item = self.value[r,c]

        if isinstance(item, list):
            score = 10 - len(item)
            score += sum(map(lambda x: 1 if isinstance(x,int) else 0, self.value[r]))
            score += sum(map(lambda x: 1 if isinstance(x,int) else 0, self.value[:,c]))
            return score
        else:
            return 0

    #检查有没错误
    def check_value(self):
        #行
        for row in self.value:
            nums = []
            lists = []
            for item in row:
                (lists if isinstance(item,list) else nums).append(item)
            if len(set(nums)) != len(nums):
                return False #数字要不重复
            if len(filter(lambda x: len(x)==0, lists)):
                return False #候选列表不能为空集

        #列
        for c in range(0,9):
            nums = []
            lists = []
            col = self.value[:,c]
            
            for item in col:
                (lists if isinstance(item,list) else nums).append(item)
            if len(set(nums)) != len(nums):
                return False #数字要不重复
            if len(filter(lambda x: len(x)==0, lists)):
                return False #候选列表不能为空集

        #九宫格
        for b_r, b_c in self.base_points:
            nums = []
            lists = []
            block = self.value[b_r:b_r+3,b_c:b_c+3].reshape(1,-1)[0]

            for item in block:
                (lists if isinstance(item,list) else nums).append(item)
            if len(set(nums)) != len(nums):
                return False #数字要不重复
            if len(filter(lambda x: len(x)==0, lists)):
                return False #候选列表不能为空集
        return True

    #猜测记录
    def recode_guess(self, point, index=0):
        #记录
        recoder = Recoder()
        recoder.point = point
        recoder.point_index = index
        #recoder.value = self.value.copy() #numpy的copy不行
        recoder.value = copy.deepcopy(self.value)
        self.recoder.put(recoder)
        self.guess_times += 1 #记录猜测次数

        #新一轮的排除处理
        item = self.value[point]
        self.value[point] = item[index]
        self.new_points.put(point)
        self.solve_sudo()

    #回溯，需要先进后出
    def reback(self):
        while True:
            if self.recoder.empty():
                raise Exception('sudo is wrong')
            else:
                recoder = self.recoder.get()
                point = recoder.point
                index = recoder.point_index + 1
                item = recoder.value[point]

                #判断索引是否超出范围。若超出，则再回溯一次
                if index < len(item):
                    break

        self.value = recoder.value
        self.recode_guess(point, index)

    #解题
    def calc(self):
        #第一次解题  
        self.solve_sudo()

        #检查有没错误的，有错误的则回溯；没错误却未解开题目，则再猜测
        while True:
            if self.check_value():
                if self.get_num_count() == 81:
                    break
                else:
                    #获取最佳猜测点
                    point = self.get_best_point()
                    
                    #记录并处理
                    self.recode_guess(point)            
            else:
                #出错，则回溯，尝试下一个猜测
                self.reback()

if __name__ == '__main__':
    #数独题目 http://cn.sudokupuzzle.org/
    #号称最难的数独
    data = [8,0,0, 0,0,0, 0,0,0,
            0,0,3, 6,0,0, 0,0,0,
            0,7,0, 0,9,0, 2,0,0,
            0,5,0, 0,0,7, 0,0,0,
            0,0,0, 0,4,5, 7,0,0,
            0,0,0, 1,0,0, 0,3,0,
            0,0,1, 0,0,0, 0,6,8,
            0,0,8, 5,0,0, 0,1,0,
            0,9,0, 0,0,0, 4,0,0]

    try:
        t1 = time.time()
        sudo = Sudo(data)
        sudo.calc()
        t2=time.time()

        print(u"完成，猜测了%s次" % sudo.guess_times)
        print(sudo.value)
        print(u"耗时：%.3fs" % (t2-t1))

    except Exception as e:
        print(e)
