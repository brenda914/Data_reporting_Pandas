
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 16:58:38 2018

@author: ltt's pc
"""

import pandas as pd


df = pd.read_csv('XXXX', encoding = 'GB2312', skiprows = 8)

dfpair = pd.read_csv('newpairuse.csv')
#dfpair = dfpair.rename(columns = {'Ad Group': 'Group','keyword':'Keywords'})

dfpaired = pd.merge(df, dfpair, on = ['关键词','推广单元','推广计划'], how = 'left')
len(df)
len(dfpaired)
dfpaired.columns

#dfpaired['Date'] = dfpaired['Date'].apply(lambda x: replace_to(x))
dfpaired['Campaign'] = 'CN: Paid SEM: Year Round 2018'
dfpaired['Source'] = 'Baidu'
result = dfpaired[['日期','Campaign','Source','Ad group','keyword', 'keyword Code','展现', '点击', '消费']]
result = result.rename(columns = {'日期': 'Date'
                                  , 'Ad group': 'Ad Group'
                                  , 'keyword': 'KeyWord'
                                  , 'keyword Code': 'SEM ID'
                                  , '展现':'Impressions'
                                  , '点击':'Clicks'
                                  , '消费':'Spending'})
result['Date'] = pd.to_datetime(result['Date'])
result['Date'] = result['Date'].dt.strftime('%m/%d/%y')
result.info()
result.to_csv('result1.csv', index = False)
print('Done')

#------------------------------------------------

df1 = pd.read_csv('jihua_20180716-20180729_387023.csv', encoding = 'GB2312', skiprows = 4)
df1['Campaign'] = 'CN: Paid SEM: Year Round 2018'
df1['Source'] = 'Baidu'

translate = {'2018三图A': 'SSF-three-image-A', '百度首页-三图-B': 'SSF-three-image-B'}

df1['Content'] = df1['推广计划'].map(translate)

df1.columns
resultif = df1[['日期','Campaign', 'Source', 'Content','展现', '点击', '消费']]

resultif = resultif.rename(columns = {'日期': 'Date'
                                      , '展现':'Impressions'
                                      , '点击':'Clicks'
                                      , '消费':'Spending'})
resultif['Date'] = pd.to_datetime(resultif['Date'])
resultif['Date'] = resultif['Date'].dt.strftime('%m/%d/%y')
resultif.to_csv('result2.csv', index = False)
print('Done')