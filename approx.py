from math import sqrt

import matplotlib.pyplot as plt
import numpy as np
import random as r

_seed = 10


def PLDistance(Point, Point_Beg, Point_End):
    p, begP, endP = np.array(Point), np.array(Point_Beg), np.array(Point_End)
    area = abs(np.cross(endP - begP, p - begP))
    bottom = sqrt((endP[0] - begP[0]) ** 2 + (endP[1] - begP[1]) ** 2)
    return area / bottom


class DP_S(object):
    def __init__(self):
        self.dslimit = dslimit
        self.qualify_list = list()
        self.disqualify_list = list()

    def dp(self, point_list):
        if len(point_list) < 3:
            self.qualify_list.extend(point_list[::-1])
        else:
            maxds_index, maxds = 0, 0
            for index, point in enumerate(point_list):
                if index in [0, len(point_list) - 1]:
                    continue

                #distance求的是三角形的高
                distance = PLDistance(point, point_list[0], point_list[-1])
                if distance > maxds:
                    maxds_index = index
                    maxds = distance
                    
            if maxds < self.dslimit:
                self.qualify_list.append(point_list[-1])
                self.qualify_list.append(point_list[0])
            else:
                sequence_Beg = point_list[:maxds_index]
                sequence_End = point_list[maxds_index:]
                for sequence in [sequence_Beg, sequence_End]:
                    if len(sequence) < 3 and sequence == sequence_End:
                        self.qualify_list.extend(sequence[::-1])
                    else:
                        self.disqualify_list.append(sequence)

    def main(self, point_list):
        self.dp(point_list)
        while len(self.disqualify_list) > 0:
            self.dp(self.disqualify_list.pop())

        qualiPts = np.array(self.qualify_list)
        plt.plot(qualiPts[:,0],qualiPts[:,1],'r')
        plt.show()

        print(self.qualify_list)
        print(len(self.qualify_list))

if __name__ == '__main__':
    dslimit = eval(input("请输入容差:"))
    ptcnt1 = eval(input("请输入点的个数:"))

    point_list = [[0] * ptcnt1] * ptcnt1
    ls = [[0] * ptcnt1] * ptcnt1
    flag = input("是否使用随机数产生坐标值：[Y/N]")
    if flag in ['y', 'Y']:
        print("随机数种子为:{}".format(_seed))
        r.seed(_seed)
        for i in range(ptcnt1):
            ls[i] = round(r.uniform(1, 100), 2)

        ls = sorted(ls, reverse=True)
        for i in range(ptcnt1):
            point_list[i] = [ls[i], round(r.uniform(1, 100), 2)]
    else:
        print("请输入坐标：[同行数字用空格分隔，不同点则用回车换行]")
        for i in range(ptcnt1):
            point_list[i] = list(map(float, input().split(" ")))
        point_list.sort(key=lambda x: x[0], reverse=True)

    plt.figure()
    pointlist = np.array(point_list)
    plt.plot(pointlist[:,0],pointlist[:,1],'-k')

    d = DP_S()
    d.main(point_list)
