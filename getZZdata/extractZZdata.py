# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:48:56 2019
将所有文件中的关于郑州的相关指标数据提取出来，放在单独的文件中。
写入文件名：年份.csv
@author: Kylin
"""

import pandas as pd

def readData(filename):
    """
    从文件中获取数据
    """
    data = pd.read_csv(filename, header = 0, usecols = [0, 1, 2, 53], encoding="utf-8")
    return data

def writeData(writefile, data):
    data.to_csv(writefile, index=False, sep=',', mode='a')

year = 2019

#文件名前缀（到月份）
file_prefix = str(year) + "\china_cities_"+str(year)
writefile = str(year) + ".csv"

#每月的天数
monthdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

#将不同月份的信息读取出来
for i in range(len(monthdays)):
    
    days = monthdays[i]
    
    for j in range(days):
        monthstr = "{:02d}".format(i+1)
        daystr = "{:02d}".format(j+1)
        filename = file_prefix + monthstr + daystr + ".csv"
        
        #获取数据数据
        data = readData(filename)
        
        #将数据写入csv文件
        writeData(writefile, data)