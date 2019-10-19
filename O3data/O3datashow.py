# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 16:01:23 2019
查看O3的数据情况
@author: Kylin
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def drawO3(data, dataIndex, msg):
    plt.figure(figsize=(25,10))
    xticks = pd.date_range(start=dataIndex.min(), end = dataIndex.max(), freq="m")
    plt.xticks(xticks, xticks.strftime("%Y/%m"), rotation=75, ha="right")
    plt.plot(data["O3"], linewidth=1)
    plt.xlabel("Time")
    plt.ylabel("scaler quantity")
    plt.title("the trend of O3 in " + msg)
    plt.show()

#1. 读取数据
filename = "O3datanew.csv"
data = pd.read_csv(filename, header = 0, encoding="utf-8")

#2. 查看数据
print("查看数据类型:\n",data.dtypes)

print("查看数据shape:\n",data.shape)

print("查看数据是否含有缺失值:\n",data.count())


#3. 将时间与小时合并成datetime字段，并设置为索引
data["hournew"] = data["hour"].map(lambda x:("%02d")%x)

data["datetime"] = data["date"].map(str) + data["hournew"].map(str)

data["datetime"] = pd.to_datetime(data["datetime"], format="%Y%m%d%H")

data["year"] = pd.DatetimeIndex(data.datetime).year
data["month"] = pd.DatetimeIndex(data.datetime).month
data["day"] = pd.DatetimeIndex(data.datetime).day

data = data.drop(["date", "hournew"], axis=1)

data = data.set_index("datetime")
#存储索引，以便后期绘图
dataIndex = data.index

#4. 调整一下数据的位置
orderlist = ["year", "month", "day", "hour", "O3", "O3_24h", "O3_8h", "O3_8h_24h"]
data = data[orderlist]
print(data.head())


#4. 查看O3数据趋势
drawO3(data, dataIndex, "all")


