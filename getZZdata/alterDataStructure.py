# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 19:17:15 2019
将数据记录按照每小时为单位进行整合，整合成含有15个测量指标的一条记录
@author: Kylin
"""
import numpy as np
import pandas as pd


def loadData(filename):
    #1. 读取源文件数据
    data = pd.read_csv(filename, header=0, encoding="utf-8")
    print("-------initialData---------")
    print(data.head())
    print("原始数据shape:", data.shape)
    m, n = data.shape
    
    #2.获取其中的信息
    date = data["date"]
    print("日期date的shape:", date.shape)

    alltype = data["type"]
    print("总type的shape:", alltype.shape)
    return data

def rechangeData(data):
    """
    转换数据
    """
    #
    indicators = ["AQI", "PM2.5", "PM2.5_24h", "PM10", "PM10_24h", "SO2", "SO2_24h", "NO2", "NO2_24h", "O3", "O3_24h", "O3_8h", "O3_8h_24h", "CO", "CO_24h"]
    
    datanew = data.loc[data.type=="AQI",["date", "hour", "郑州"]]
    datanew.rename(columns = {"郑州":"AQI"}, inplace=True)
    
    for i in range(1, len(indicators)):
        #先找到AQI的
        subdata = data.loc[data.type==indicators[i], ["date","hour", "郑州"]]
        subdata.rename(columns={"郑州":indicators[i]}, inplace=True)
        datanew = pd.merge(datanew, subdata, how="left", on=["date", "hour"])
    
    return datanew

def writeData(writefile, data):
    """
    将修改后的数据写入文件
    """
    data.to_csv(writefile, index=False, sep=',', mode='a')
    
if __name__ == "__main__":
    filename = "2019.csv"
    writefile = "changed" + filename
    data = loadData(filename)
    datanew = rechangeData(data)
    writeData(writefile, datanew)