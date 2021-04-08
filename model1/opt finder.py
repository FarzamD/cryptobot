import pandas as pd
import time
def dict_remove(d,ks):
    res=[]
    for key in ks:
        try:
            d.pop(key)
        except:
            res.append(key)
    return res
temp=''
exec('temp='+str(open('4k.json').read())+"['data']['cryptoCurrencyList']")
data=[]

for data_row in temp:
    tmp=data_row.copy()
    dict_remove(tmp, ['ath','atl','atc','id','lastUpdated','dateAdded','slug'])
    dict_remove(tmp['quotes'][0], ['lastUpdated','percentChange1h','percentChange7d','percentChange60d','marketCap','fullyDilluttedMarketCap','volume7d','volume30d','volume24h'])
    dict_remove(tmp['quotes'][1], ['lastUpdated','percentChange1h','percentChange7d','percentChange60d','marketCap','fullyDilluttedMarketCap','volume7d','volume30d','volume24h'])
    dict_remove(tmp['quotes'][2], ['lastUpdated'])
    data.append(tmp)

data2=[]
exec('temp='+str(open('2k10m.json').read())+"['data']['cryptoCurrencyList']")

for data_row in temp:
    a=data_row['quotes'][2].copy()
    tmp=dict(name=data_row['name'],symb=data_row['symbol'],date=a['lastUpdated'],price=a['price'], marketCap=a['marketCap'],
             dP7d=a['percentChange7d'] ,dP24h=a['percentChange24h'] ,dP30d=a['percentChange30d'] ,dP60d=a['percentChange60d'] ,dP90d=a['percentChange90d'])
    tmp['id']=data_row['id']
    data2.append(tmp)
p=pd.DataFrame(data2)
name=f'2k {time.strftime("%d %b %Y")}.csv'
p.to_csv(name)
'''
w=pd()
pools_bs=w.findAll('tr')

def columniator(table,header=False):
    if header:
        temp=table.findAll('th')
    else:
        temp=table.findAll('td')
    res=[]
    for i in temp:
        res.append(i.text.strip())
    return res
header=columniator(pools_bs.pop(0),True)
pools=[]
for pool in pools_bs:
    temp={}
    p=columniator(pool)
    for i in range(len(header)):
        temp[header[i]]=p[i]
    pools.append(temp)
p=pd.DataFrame(pools).set_index('')
p.to_csv('week.csv')
'''

#table=soup.find('table',{'class':'infoboxtable'}).findAll('tr')


