import os
import pandas as pd
import numpy as np
import schedule
import requests
import time

def get2k_cryptos():
    hdr={ "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
     ,"Connection": "keep-alive"}

    data={"start":"1","limit":"2000","sortBy":"market_cap","sortType":"desc","convert":"USD,btc,eth",
     "cryptoType":"all","tagType":"all","aux":"ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,volume_7d,volume_30d"}
    url='https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=100&sortBy=market_cap&sortType=desc&convert=USD,btc,eth&cryptoType=all&tagType=all&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,volume_7d,volume_30d'
    s=requests.Session()
    g=s.get(url,data=data)
    res=g.json()['data']
    return res
a= get2k_cryptos()
cryptos = []
def crypto_json2DF(j):
    k=[ 'name', 'symbol', 'slug', 'tags', 'circulatingSupply', 'totalSupply', 'isActive', 'dateAdded']
    dk=[ 'price', 'marketCap', 'percentChange1h', 'percentChange24h', 'percentChange7d', 'percentChange30d', 'percentChange60d', 'percentChange90d', 'dominance', 'ytdPriceChangePercentage']
    res=[]
    for i in j['cryptoCurrencyList']:
        tmp={key:i[key] for key in k}
        for key in dk:
            tmp[key]=i['quotes'][2][key]
        res.append(tmp)
    return res
cryptos=crypto_json2DF(a)
cryptos=pd.DataFrame(cryptos)

def cap_price_filter(data, filt):
    res=data
    if filt['price']:
        res=res[res['price']>filt['price'][0]]
        res=res[res['price']<filt['price'][1]]
    if filt['marketCap']:
        res=res[res['marketCap']>filt['marketCap'][0]]
        res=res[res['marketCap']<filt['marketCap'][1]]
    return res
#def crypto_statiator(data):

priceRange=[(0,1e-3),(1e-4,1e-2),(1e-3,1e-1),(1e-2,1),(1e-1,1e1),(1,1e2) ]
marketCapRange=[(1e6,1e8),(1e7,1e9),(1e8,1e6),(1e9,1e11)]
grids=[]
for i in range(6):
    for j in range(4):
        p=priceRange[i]
        mc=marketCapRange[j]
        temp={'name':f'price{p},mkCap{mc}','price':p,'marketCap':mc}
        td=cap_price_filter(cryptos, temp)#temp data
        if td.size>300:
            td2=td.sort_values('percentChange30d').tail(15)
#            temp={'24h_var':td['percentChange24h'].var(),'24h_avg':td['percentChange24h'].mean(),'7d_var':td['percentChange7d'].var(),'7d_avg':td['percentChange7d'].mean(),            '30d_var':td['percentChange30d'].var(),'30d_avg':td['percentChange30d'].mean(),'60d_var':td['percentChange60d'].var(),'60d_avg':td['percentChange60d'].mean(),'90d_var':td['percentChange90d'].var(),'90d_avg':td['percentChange90d'].mean()}
#            temp={'24h_var':td2['percentChange24h'].var(),'24h_avg':td2['percentChange24h'].mean(),'7d_var':td2['percentChange7d'].var(),'7d_avg':td2['percentChange7d'].mean(),            '30d_var':td2['percentChange30d'].var(),'30d_avg':td2['percentChange30d'].mean(),'60d_var':td2['percentChange60d'].var(),'60d_avg':td2['percentChange60d'].mean(),'90d_var':td2['percentChange90d'].var(),'90d_avg':td2['percentChange90d'].mean()}
            temp={'7d_avg top':td2['percentChange7d'].mean(), '30d_avg top':td2['percentChange30d'].mean(), '60d_avg top':td2['percentChange60d'].mean(), '90d_avg top':td2['percentChange90d'].mean(), 
                  '7d_avg':td['percentChange7d'].mean(), '30d_avg':td['percentChange30d'].mean(), '60d_avg':td['percentChange60d'].mean(), '90d_avg':td['percentChange90d'].mean()}
            temp['name']=f'price{p},mkCap{np.int8(np.log10(mc))}'
            temp['7d_score']=temp['7d_avg']+temp['7d_avg top']**(2/3)
            temp['30d_score']=temp['30d_avg']+temp['30d_avg top']**0.75
            temp['60d_score']=temp['60d_avg']+temp['60d_avg top']**0.8
            temp['90d_score']=temp['90d_avg']+temp['90d_avg top']**0.85
            grids.append(temp)
p=pd.DataFrame(grids)
name=f'opt {time.strftime("%d %b %Y")}.csv'
p.sort_values('30d_score').head(12).to_csv(name)

k=[ 'name', 'symbol', 'slug', 'tags', 'circulatingSupply', 'totalSupply', 'dateAdded']
dk=[ 'price', 'marketCap', 'percentChange1h', 'percentChange24h', 'percentChange7d', 'percentChange30d', 'percentChange60d', 'percentChange90d', 'dominance', 'ytdPriceChangePercentage']



d=[]
start="1603326100"
end="1616286100"

schedule.every(0.15).seconds.do(DLcoin)
while (i<last_i):
    schedule.run_pending()

for i in range(50):
    s=requests.Session()
    coin=chosen.iloc[i,:]
    print(coin['name'])
    coinData={"convert":"USD" ,"format":"chart_crypto_details", "interval":"2h"
    ,"id":coin['id']  ,"time_end":end,"time_start":start}
    url='https://web-api.coinmarketcap.com/v1.1/cryptocurrency/quotes/historical?'
    url+= f'convert={coinData["convert"]}&format=chart_crypto_details&id={coinData["id"]}&interval=2h&'
    url+= f'time_end={end}&time_start={start}'
    g=s.get(url,data=coinData)
    a=g.json()['data']
    tmp={'name':coin['name'],'rank': coin['Unnamed: 0'], 'id':coin['id'],
         'sym':coin['symb'],'marketCap':coin['marketCap']}
    for key in a.keys():
        tmp[key.split('.')[0][:-4]+'0']= a[key]['USD'][0]
    d.append(tmp)

p=pd.DataFrame(d)

from matplotlib import pyplot as plt
n=10
di=50//n
keys=[]

for i in range(49//di+1):
    keys.append(range(i*di,min(50,(i+1)*di)))
for i in keys:
    pt=p.set_index('name').transpose()
    pt=pt.iloc[4:,i]
    ls=pt.index.values
    '''labels=np.arange(259//8)
    x=[ls[i*8] for i in labels]
    labels=[l.split('T')[0][2:] for l in x]'''
    ax=pt.plot()
    x=np.arange(0,359,13)
    ax.set_xticks(x)
    labels=[ls[l].split('T')[0][2:] for l in x]
    ax.set_xticklabels(labels,rotation=30)
    ax.figure.set_size_inches([18,12])
    ylim=ax.get_ylim()
    yt=np.linspace(ylim[0],ylim[1],37)
    ax.set_yticks(yt)
    ax.grid()
    ax.figure.savefig(f'{i.start}-{i.stop}.png')
for i in keys[0]:
    coin=p.iloc[i,4:]
    coinName=p.iloc[i,0]
    plt.plot()



###############################################################3


import cv2
import requests
import numpy as np                 
data = {"login":"my_login", "password":"my_password"}
purl='https://portal.aut.ac.ir/aportal/'
hdr={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'}
url='https://portal.aut.ac.ir/aportal/PassImageServlet'

def stringed(n):
    n2=(n%100)//10
    return str(n//100)+str(n2)+str(n%10)

def feature(img):
    return cv2.Canny(img,50,50)


def DLimg():
    s = requests.Session()
    r = s.post(purl,headers=hdr)
    ck=r.cookies.copy() 
    global i
    img=s.post(url,headers=hdr,cookies=ck)
    img_inB=np.asanyarray(bytearray(img.content),dtype='uint8')
    finalimg=cv2.imdecode(img_inB,cv2.IMREAD_UNCHANGED) 
    n=stringed(i)
    cv2.imwrite('captcha_'+n+'.png',feature(finalimg))
    i+=1



schedule.every(0.25).seconds.do(DLimg)
while (i<end):
    schedule.run_pending()



