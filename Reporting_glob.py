# -*- coding: utf-8 -*-
"""
Created on Thu May 17 11:23:10 2018

@author: ltt
"""

import glob
import pandas as pd

# Select all the files in your directory, make sure only the 360 data are at the dir
# no chinese characters in the directory
# no chinese characters in the filename
# make sure to change the word directory
# if the match type has changed you need to generate a new pairuse file which is write in ''' '''
directory = r'C:\Users\tli06\Documents\iProspect_li\Tuesday\0724_0730\k360'
file_names = glob.glob(directory + "/*.csv")

len(file_names)
print(file_names)

list_all = []
for file_name in file_names:
    df = pd.read_csv(file_name, encoding = 'gbk')
    list_all.append(df)
    



df360 = pd.concat(list_all)

test = pd.read_csv(r'C:\Users\tli06\Documents\iProspect_li\Tuesday\360pairuse.csv')

paired = pd.merge(df360, test\
                      , left_on=['推广计划', '推广组', '关键词']\
                      , right_on = ['推广计划名称', '推广组名称', '关键词']\
                      , how = 'left')

paired['Site'] = 'PC'
paired['URL'] = 'http://www.accorhotels.com'
paired['CTR'] = ''
paired['CPC'] = ''

resultzhu = paired[paired['推广账户']=='雅高酒店2014']\
            [['日期','Site', 'URL', '推广计划', '推广组', '关键词匹配模式', '关键词'\
              , '展示次数', '点击次数', 'CTR', 'CPC','总费用']]
resulth = paired[paired['推广账户']!='雅高酒店2014']\
            [['日期','Site', 'URL', '推广计划', '推广组', '关键词匹配模式', '关键词'\
              , '展示次数', '点击次数', 'CTR', 'CPC','总费用']]
match = {'短语': 'Phrase', '智能短语': 'Phrase', '精确': 'Exact'} 

resultzhu['关键词匹配模式'] = resultzhu['关键词匹配模式'].map(match)
           
resulth['关键词匹配模式'] = resulth['关键词匹配模式'].map(match)
resulth = resulth[resulth['关键词匹配模式'].notnull()] 



resultzhu['日期'] = pd.to_datetime(resultzhu['日期'])
resultzhu['日期'] = resultzhu['日期'].dt.strftime('%Y/%m/%d')
resultzhu.columns = ['Date','Site', 'URL','Campaign','Ad Group','Matche Type','Keywords','Impression','Clicks','CTR','CPC','Cost']

resulth['日期'] = pd.to_datetime(resulth['日期'])
resulth['日期'] = resulth['日期'].dt.strftime('%Y/%m/%d')
resulth.columns = ['Date','Site', 'URL','Campaign','Ad Group','Matche Type','Keywords','Impression','Clicks','CTR','CPC','Cost']

resultzhu.to_csv('360_Data_20180730.txt', sep = '\t', index = False)
resulth.to_csv('h360_Data_20180730.txt', sep = '\t', index = False)
print('Done!')

print('主账户消费')
print(resultzhu.Cost.sum())
print('海外消费')
print(resulth.Cost.sum())






