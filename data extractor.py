import numpy as np
import requests
import pandas as pd
def getCryptoNames(price,marketCap):
    s=requests.Session()
    url='https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=250&sortBy=market_cap&sortType=desc&convert=USD,btc,eth&cryptoType=all&tagType=all&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,volume_7d,volume_30d'
    url+=f'&priceRange={price[0]}~{price[1]}&marketCapRange={marketCap[0]}~{marketCap[1]}'
    g=s.get(url)
    g=g.json()['data']['cryptoCurrencyList']
    res=[{'name':i['name'], 'id':i['id'],'marketCap':i['quotes'][2]['marketCap'],'sym':i['symbol'],'ch30d':i['quotes'][2]['percentChange30d'],'price':i['quotes'][2]['price']}for i in g]
    return res

def meine_classifier(percentChange30d):
    if percentChange30d<40: return 0
    elif percentChange30d<125: return 1
    elif percentChange30d<275: return 2
    else: return 3

def getCryptoData(crypto_Names):
    endt="1609542500"
    day=89600
    month=2593100
    monthx3=7779300
    startt3m= str(int(endt)-monthx3)
    startt24h=str(int(endt)-day)
    res={}
    for coin in crypto_Names:
        try:
            s=requests.Session()
            coinData={"convert":"USD" ,"format":"chart_crypto_details", "interval":"4h"
            ,"id":coin['id']  ,"time_end":endt,"time_start":startt3m}
            print(coin['id'])
            url='https://web-api.coinmarketcap.com/v1.1/cryptocurrency/quotes/historical?'
            url+= f'convert={coinData["convert"]}&format=chart_crypto_details&id={coinData["id"]}&interval=4h&'
            url+= f'time_end={endt}&time_start={startt3m}'
            g=s.get(url,data=coinData)
            a=g.json()['data']
            tmp={'name':coin['name'], 'id':coin['id'],'ch30d':coin['ch30d'],'y':meine_classifier((coin['ch30d'])),
                 'sym':coin['sym'],'marketCap':coin['marketCap']}
            tmp['30d']=[a[key]['USD'][0] for key in a.keys()]
            res[tmp['name']]=tmp
        except:
            print(coin['name']+'   fucked up')
    for coin in crypto_Names:
        try:
            s=requests.Session()
            coinData={"convert":"USD" ,"format":"chart_crypto_details", "interval":"5m"
            ,"id":coin['id']  ,"time_end":endt,"time_start":startt24h}
            print(coin['name'])
            url='https://web-api.coinmarketcap.com/v1.1/cryptocurrency/quotes/historical?'
            url+= f'convert={coinData["convert"]}&format=chart_crypto_details&id={coinData["id"]}&interval=5m&'
            url+= f'time_end={endt}&time_start={startt24h}'
            g=s.get(url,data=coinData)
            a=g.json()['data']
            res[coin['name']]['24h']=[a[key]['USD'][0] for key in a.keys()]
        except:
            print(coin['name']+'   fucked up')
    return res

cryptos=getCryptoNames((1e-6,0.05),[int(1e6),int(1e9)])
d= getCryptoData(cryptos)

def dataset_formatter(ds):
    res=[]
    for key in ds.keys():
        coin=d[key]
        res.append( [meine_classifier(coin['ch30d']),np.power((100+coin['ch30d'])/100,0.5) ,(100+coin['ch30d'])/100,coin['name'], coin['id'] ]+coin['30d']+coin['24h'])
    res=pd.DataFrame(res)
    return res
'''
ds=pickle.load(open('ds.pickle','rb'))
ds=pd.DataFrame(ds)
'''
ds= dataset_formatter(d)
