# -*- coding: utf-8 -*-


import pandas as pd





pcbrz = pd.read_excel('ReportXXX.xlsx', sheet_name = 1)
mbbrz = pd.read_excel('ReportXXX.xlsx', sheet_name = 1)
zhidaobrz = pd.read_excel('ReportXXX.xlsx', sheet_name = 1)
dingtubrz = pd.read_excel('ReportXXX', sheet_name = 1)
shipinbrz = pd.read_excel('ReportXXX', sheet_name = 1)
mapbrz = pd.read_excel('ReportXXX', sheet_name = 1)


print(str(70-len(pcbrz))+ ' of pcbrz are missing')
print(str(70-len(mbbrz))+ ' of mbbrz are missing')
pcbrz.groupby('Ad_Group')['Date'].count()
mbbrz.groupby('Ad_Group')['Date'].count()



#add back the days wthout impressions
#it would be quick if doing it manually
#read in the budget sheet
dfcost = pd.read_excel('BrandZone_ReportingFile.xlsx', sheet_name = 'cost')

pcbrz['Date'] = pd.to_datetime(pcbrz['Date'])
ppc_pc = pd.DataFrame(pcbrz.groupby('Date')['imp'].sum())
ppc_pc.reset_index(inplace = True)
tempc = pd.merge(ppc_pc, dfcost, how = 'left', on = 'Date')
ppc_pc['ppc'] = tempc['pcbrz_Budget']/tempc['imp']
ppc_pc.drop('imp', axis=1, inplace = True)
pcbrzppc = pd.merge(pcbrz, ppc_pc, on = 'Date', how = 'left')
#pcbrzppc.head()  
pcbrz['cost'] = pcbrzppc['imp']*pcbrzppc['ppc']




mbbrz['Date'] = pd.to_datetime(mbbrz['Date'])
pmb_mb = pd.DataFrame(mbbrz.groupby('Date')['imp'].sum())
pmb_mb.reset_index(inplace = True)
temmb = pd.merge(pmb_mb, dfcost, how = 'left', on = 'Date')
pmb_mb['pmb'] = temmb['mbbrz_Budget']/temmb['imp']
pmb_mb.drop('imp', axis=1, inplace = True)
mbbrzpmb = pd.merge(mbbrz, pmb_mb, on = 'Date', how = 'left')
#mbbrzpmb.head()  
mbbrz['cost'] = mbbrzpmb['imp']*mbbrzpmb['pmb']


brz = pd.concat([pcbrz, mbbrz])
#brz.columns
#len(brz)
#read the excel file used to get the name and budget
pairuse = pd.read_excel('BrandZone_ReportingFile.xlsx', sheet_name = 0)

brzpm = pd.merge(brz, pairuse, left_on = 'Ad_Group', right_on = 'adgroup', how = 'left')
len(brzpm)
brzpm.tail()
brzpm = brzpm.rename(columns={'Date': 'date'
                            , 'imp':'impressions'
                            , 'clicks':'clicks'
                            })

brzpm.columns
brzpm['channel'] = 4999
brzpm['match_type'] = 'Exact'
brzpm['currency_code'] = 'CNY'
brzpm1 = brzpm[['date'
               , 'channel'
               , 'campaign'
               , 'adgroup'
               , 'keyword'
               , 'match_type'
               , 'impressions'
               , 'clicks'
               , 'cost'
               , 'currency_code']]

#merge the dataframe to get the budget for map campaigns


print('should be 21 and get '+ str(len(mapbrz)))
mapbrz.head()
#mapdanyuan = mapbrz['Ad_Group'].unique().tolist()
#print(mapdanyuan)
#mapdanyuan[0]
#mapdanyuan[1]
#mapdanyuan[2]
mapbrz['Date'] = pd.to_datetime(mapbrz['Date'])
mapbrz.loc[mapbrz['Ad_Group']=='20180411_165708_品牌专区-网页地图', 'pk'] = 'pcmap'
mapbrz.loc[mapbrz['Ad_Group']=='20180411_165708_品牌专区-无线地图', 'pk'] = 'mobmap'
mapbrz.loc[mapbrz['Ad_Group']=='20180411_165708_品牌专区-NA地图', 'pk'] = 'namap'
temmap = pd.merge(mapbrz, dfcost, how = 'left', on = 'Date')
mapbrz['cost'] = temmap['map_Budget']
#len(mapbrz)
#mapbrz.tail()



#NS zhidao dingtu shipin have the same daily expense

print('should be 7 and get '+ str(len(zhidaobrz)))
print('should be 7 and get '+ str(len(dingtubrz)))
print('should be 7 and get '+ str(len(shipinbrz)))

#shipinbrz
zhidaobrz['pk'] = 'zhidao'
dingtubrz['pk'] = 'dingtu'
shipinbrz['pk'] = 'shipin'

#merge ns sd campaigns with the excel file to get the name and structure of the data 
nsxiao = pd.concat([zhidaobrz,dingtubrz,shipinbrz])
nsxiao['Date'] = pd.to_datetime(nsxiao['Date'])

temxiao = pd.merge(nsxiao, dfcost, how = 'left', on = 'Date')
nsxiao['cost'] = temxiao['ns_Budget']

#nsxiao.reset_index(inplace = True)
#nsxiao.drop('index', axis =1,inplace = True)
pairns = pd.read_excel('BrandZone_ReportingFile.xlsx', sheet_name = 1)
ns = pd.concat([mapbrz, nsxiao])
#ns.tail()
nsbrz = pd.merge(ns, pairns, on = 'pk', how = 'left')






nsbrz = nsbrz.rename(columns={'Date': 'date'
                            , 'imp':'impressions'
                            , 'clicks':'clicks'
                            })

nsbrz.columns
nsbrz['channel'] = 4999
nsbrz['match_type'] = 'Exact'
nsbrz['currency_code'] = 'CNY'
nsbrz1 = nsbrz[['date'
               , 'channel'
               , 'campaign'
               , 'adgroup'
               , 'keyword'
               , 'match_type'
               , 'impressions'
               , 'clicks'
               , 'cost'
               , 'currency_code']]

#concat the two part of the brandzone report
finalbrz = pd.concat([brzpm1,nsbrz1])
#finalbrz['date'] = pd.to_datetime(finalbrz['date'])
finalbrz.sort_values(by = ['adgroup','date'], inplace =True)
finalbrz['date'] = finalbrz['date'].dt.strftime('%m/%d/%Y')

sog = pd.read_excel('BrandZone_ReportingFile.xlsx', sheet_name = 'sogou360temp')
finalbrz.reset_index(inplace = True, drop = True)
sog['date'] = finalbrz.loc[:35,'date']
dfcost['Date'] = dfcost['Date'].dt.strftime('%m/%d/%Y')
sog1 = pd.merge(sog, dfcost, left_on = 'date', right_on = 'Date', how = 'left')
#sog1 = pd.concat([sog, dfcost], axis = 0)
sog.loc[sog['keyword']=='360 PC BrandZone', 'cost'] = sog1['360_Budget']
sog.loc[sog['keyword']=='Sogou PC BrandZone', 'cost'] = sog1['sogPC']
sog.loc[sog['keyword']=='Accor Mobile BrandZone', 'cost'] = sog1['sogMB']

brandzone = pd.concat([finalbrz, sog])
brandzone.to_csv('baidubrz.csv', index = False)
#len(finalbrz)
print('Done!')

print('Check your work dir.')

#finalbrz.cost.sum()







