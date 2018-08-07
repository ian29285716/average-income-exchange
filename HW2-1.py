import matplotlib 
import matplotlib.pyplot as plt
import requests
import json
import pandas as pd
import csv
import re
import pipreqs

def get_oilprice():
    oil_url = 'https://www.quandl.com/api/v3/datasets/BP/CRUDE_OIL_PRICES.json?api_key=9cLNX2qEVMTZaRysiv7_'
    oil_r=requests.get(oil_url)
    oil_response = (oil_r.json())

    with open('oil_r.json','w',encoding='utf-8-sig') as f_oi:
        json.dump(oil_response,f_oi)

def average_ni():
    average_NI= "https://www.dgbas.gov.tw/public/data/dgbas03/bs4/nis93/np02.xls"
    average= requests.get(average_NI)
 
    output = open('average.xls', 'wb')
    output.write(average.content)
    output.close()

    data_xls = pd.read_excel('average.xls', 'P2', index_col=None)
    data_xls.to_csv('average_ni', encoding='utf-8-sig')

def exchange():
    url = 'https://quality.data.gov.tw/dq_download_json.php?nid=6563&md5_url=ea67c565f721b6920a1982599526ed0b'

    r=requests.get(url)
    response = (r.json())

    with open('exchange.json','w',encoding='utf-8-sig') as f_ex:
        json.dump(response,f_ex)

    with open('exchange.json','r',encoding='utf-8-sig') as f_exs:
        exchange=json.loads(f_exs.read())
        n=len(exchange)
        n1=n-1
        with open('exchange.csv','w',encoding='utf-8-sig') as fw:
            filewriter = csv.writer(fw, delimiter=',')
            filewriter.writerow(['YEAR','NTD:USD','JPY:USD','CNY:USD'])
            for i in range(0,n1):
                YEAR=exchange[i]['期間']
                NTD=exchange[i]['新台幣NTD/USD']
                JPY=exchange[i]['日圓JPY/USD']
                CNY=exchange[i]['人民幣CNY/USD']
                filewriter.writerow([YEAR,NTD,JPY,CNY])


def price():
    average_price= "https://www.stat.gov.tw/public/data/dgbas03/bs3/inquire/cpispl.xls"
    average= requests.get(average_price)
 
    output = open('average_price.xls', 'wb')
    output.write(average.content)
    output.close()

    data_xls = pd.read_excel('average_price.xls', 'CPI', index_col=None)
    data_xls.to_csv('average_price', encoding='utf-8-sig')

exchange()


average_ni()
list_average_ni_year=[]
list_average_ni_income=[]
with open('average_ni', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    headers = next(f)
    headers = next(f)
    for row in reader:
        year=re.search('\d+',row[0])
        income=re.search('\d+',row[8])
        if year!=None:
            list_average_ni_year.append(int(year.group())+1911)
        if income!=None:
            list_average_ni_income.append(int(income.group())/12)

price()
with open('average_price', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(f)
        headers = next(f)
        list_CPI_year=[]
        list_CPI_number=[]
        for row in reader:
            year=re.search('\d+',row[1])
            CPInumber=re.search('[0-9]+\.*[0-9]*',row[14])
            if year!=None and int(year.group())>40:
                list_CPI_year.append(int(year.group())+1911)
            if CPInumber!=None:
                list_CPI_number.append(float(row[14]))

exchange()
with open('exchange.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(f)
        list_exchange_year=[]
        list_exchange_number=[]
        for row in reader:
            if row!=[]:
                list_exchange_year.append(int(row[0]))
                list_exchange_number.append(float(row[1]))

get_oilprice()
with open('oil_r.json','r',encoding='utf-8-sig') as f:
    oil=json.loads(f.read())
    n=len(oil["dataset"]["data"])
    n1=n-1
    list_oil_year=[]
    list_oil_ori=[]
    list_oil_priinf=[]
    for i in range(0,n1):
        oil_year=re.search('\d+',oil["dataset"]["data"][i][0])
        list_oil_year.append(int(oil_year.group()))
        list_oil_ori.append(float(oil["dataset"]["data"][i][1]))
        list_oil_priinf.append(float(oil["dataset"]["data"][i][2]))



dict1 = {'year': list_average_ni_year,'average_ni':list_average_ni_income}
df1 = pd.DataFrame(dict1)

dict2 = {'year': list_CPI_year,'CPI':list_CPI_number}
df2 = pd.DataFrame(dict2)

dict3 = {'year': list_exchange_year,'Exchange':list_exchange_number}
df3 = pd.DataFrame(dict3)

dict4 = {'year': list_oil_year,'oil_ori':list_oil_ori,'oil_priinf':list_oil_priinf}
df4 = pd.DataFrame(dict4)

df_g1 = pd.merge(df1,df2, on='year', how='outer')
data1=df_g1.dropna()

df_g2 = pd.merge(df1,df3, on='year', how='outer')
data2=df_g2.dropna()

df_g3 = pd.merge(df1,df4, on='year', how='outer')
data3=df_g3.dropna()
print(data3)

plt.plot(list_average_ni_year,list_average_ni_income,color='blue',linewidth=2.0)
plt.plot(data1['year'],data1['average_ni']/data1['CPI']*100,color='red',linewidth=2.0)
plt.plot(data2['year'],data2['average_ni']/data2['Exchange']*32,color='green',linewidth=2.0)
plt.plot(data3['year'],data3['average_ni']*43*32/(data2['Exchange']*data3['oil_ori']),color='pink',linewidth=2.0)
plt.title(u'國民平均月所得')
plt.xlabel(u'年(西元)')
plt.ylabel(u'       金額(新台幣)       ',rotation=360)
plt.show()

pipreqs ./