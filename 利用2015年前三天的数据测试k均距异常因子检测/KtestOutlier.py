# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:39:54 2019
K均距异常检测的实现
@author: Kylin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def loadData(filename):
    """
    加载数据集
    参数：
        filename文件名
    """    
    data = pd.read_csv(filename, header=0, encoding="utf-8")
    return data

def dataProcess(data):
    """
    对原始数据进行一些加工处理
    参数：
        原始数据
    返回值：
        修改后的data，数据索引dataIndex
    """
    #1. 对时间进行处理
    data["hournew"] = data["hour"].map(lambda x:("%02d")%x)
    data["datetime"] = data["date"].map(str) + data["hournew"].map(str)
    data["datetime"] = pd.to_datetime(data["datetime"], format="%Y%m%d%H")
    data["year"] = pd.DatetimeIndex(data.datetime).year
    data["month"] = pd.DatetimeIndex(data.datetime).month
    data["day"] = pd.DatetimeIndex(data.datetime).day
    data = data.drop(["date", "hournew"], axis=1)
    
    #2. 将datetime字段设置为数据索引
    data = data.set_index("datetime")
    #存储索引，以便后期绘图
    dataIndex = data.index
    
    #3. 调整数据位置
    orderlist = ["year", "month", "day", "hour", "O3", "O3_24h", "O3_8h", "O3_8h_24h"]
    data = data[orderlist]
    
    return data, dataIndex

def plotInitial(data, dataIndex, msg):
    """
    绘制原始数据图像
    """
    plt.figure(figsize=(25,10))
    xticks = pd.date_range(start=dataIndex.min(), end = dataIndex.max(), freq="m")
    plt.xticks(xticks, xticks.strftime("%Y/%m"), rotation=75, ha="right")
    plt.plot(data["O3"], linewidth=1, alpha=0.9)
    plt.xlabel("Time")
    plt.ylabel("scaler quantity")
    plt.title(msg)
    plt.show()


def getwindowOutlierIndex(windowarray, w, start):
    """
    计算给定窗格中的异常数据
    参数：
        windowarray:窗口数据
        w:窗口大小
        start:窗口数据的开始索引
    返回值：
        pointlist:异常数据元素索引列表
    """
    wmin = windowarray.min()
    wmax = windowarray.max()
    wstd = windowarray.std()
    
    pointnum = 0
    pointlist = []
    
    for i in range(w):
        if windowarray[i] > wmax - wstd:
            pointnum += 1
            #如果这个点疑似异常点，存储其下标
            pointlist.append(start + i)
    
    print("异常数据有:", pointnum, "个")
    print("异常数据的下标是:", pointlist)
    
    return pointlist

def getMiddleWeight(windowarray):
    

def drawOutlier(data):
    """
    """

def testOutlier(outlierarray, pointlist):
    """
    用于异常点检测
    返回：
        计算后的异常点数组
    """
    for i in range(len(pointlist)):
        #当异常元素出现的时候，就将这个异常元素下标的索引对应的值加1
        outlierarray[pointlist[i]] += 1
    return outlierarray



def getWeight(data, w):
    """
    边缘权重因子的计算：用于确定子时间序列的边界点
    参数：
        data:数据
        w:窗口宽度
    """
    #定义wlist，用于存储异常元素下标
    wlist = []
    
    #假设使用前80条数据用于测试
    datatest = data[["O3"]].iloc[:80]
    datatestIndex = datatest.index
    
    #查看这80条数据的图像情况
    plotInitial(datatest, datatestIndex, "the trend of test O3 data")
    
    #为了便于处理，将dataFrame类型的数据转化为ndarray类型
    testarray = datatest.values
    
    #对第一个窗口和最后一个窗口的元素单独处理
    forewindowarray = testarray[:w]
    endwindowarray = testarray[len(testarray)-w:]
    forewindowpointlist = getwindowOutlierIndex(forewindowarray, w, 0)
    endwindowpointlist = getwindowOutlierIndex(endwindowarray, w, len(testarray)-w)
    
    #定义一个数组，用来存放异常点出现的次数
    outlierarray = np.zeros_like(testarray)
    
    

if __name__ == "__main__":
    #1.加载数据
    filename = "2015O3data.csv"
    data = loadData(filename)
    
    #2. 对原始数据做一些处理
    data, dataIndex = dataProcess(data)
    
    #3. 绘制原始数据图像
    plotInitial(data, dataIndex, "The trend of O3 in 2015")
    
    #4. 计算边缘权重因子，找到子时间序列的边界点
    w = 12
    getWeight(data, w)
    