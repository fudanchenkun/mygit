#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data1=pd.read_csv(r'/home/chenkun/Desktop/ppd2015.csv',header=None)
data1.columns=['bidid','investor','rate','money','date','time','timelong']
data2=pd.read_csv(r'/home/chenkun/Desktop/ppd201504.csv',header=None)
data2.columns=['bidid','time1','time2']

temp1=pd.merge(data1,data2.loc[:,['bidid']],how='inner',on='bidid')

temp2=temp1['date']+' '+temp1['time']

temp1['timestamp']=temp2

temp1=temp1.loc[:,['bidid', 'investor', 'rate', 'money', 'timelong','timestamp']]

timequantum=map(lambda x:x.split(' ')[1].split(':')[0],temp1['timestamp'])

temp2=pd.DataFrame({'timequantum':map(int,timequantum),
                   'count':''})

temp2pic=temp2.groupby('timequantum').count()

temp2pic.plot(kind='bar')

plt.plot(temp2pic.index,temp2pic['count'].values,'bp--')
plt.show()