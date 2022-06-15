import pandas as pd
import numpy as np
import datetime

city_code = {
    "基隆市": "KEE",
    "新北市": "NWT",
    "台北市": "TPE",
    "桃園市": "TAO",
    "新竹市": "HSZ",
    "新竹縣": "HSQ",
    "苗栗縣": "MIA",
    "台中市": "TXG",
    "彰化縣": "CHA",
    "南投縣": "NAN",
    "雲林縣": "YUN",
    "嘉義縣": "CYQ",
    "嘉義市": "CYI",
    "台南市": "TNN",
    "高雄市": "KHH",
    "屏東縣": "PIF",
    "宜蘭縣": "ILA",
    "花蓮縣": "HUA",
    "台東縣": "TTT",
    "澎湖縣": "PEN",
    "金門縣": "KIN",
    "連江縣": "LIE",
    "全國": "TW"
}

def parseDiagnoseData(filename):
    diaDf = pd.read_csv(filename,encoding='Big5')
    diaDf.columns=[
            'index', 'guessDate', 'date', 'city', 'section', 'count', 'accumulateCount'   ]
    diaDf = diaDf[diaDf['section']=='全區']
    diaDf = diaDf[diaDf['city']!='境外移入']

    diaDf.reset_index(inplace = True)

    diaDf = diaDf[['city', 'date', 'count', 'accumulateCount']]

    #for i in range(diaDf.shape[0]):
    #    time = diaDf.iloc[i].loc['date'].split('/')
    #    diaDf.loc[i, 'date'] = time[0] + '-' + "%02d" % int(time[1]) + '-' + "%02d" % int(time[2])

    # Rename city
    diaDf.loc[:, 'city'] = diaDf['city'].map(lambda x: city_code[x])

    return diaDf


def addDate(diaDf):
    
    start_date = datetime.datetime.strptime("20200128", "%Y%m%d")
    end_date = datetime.datetime.strptime("20220607", "%Y%m%d")
   
    n_city = len(city_code)
    n_date = int((end_date - start_date).days) + 1
    print(n_city, n_date)

    newDf = pd.DataFrame(columns = ['city', 'date', 'count', 'accumulateCount'])
    for i in range(n_date):
        now_date = str(start_date + datetime.timedelta(days=i)).split(' ')[0]
        if now_date in diaDf['date'].values:
            nowDf = diaDf[diaDf['date']==now_date]
            for city in city_code:
                if city_code[city] in nowDf['city'].values:
                    df = diaDf[(diaDf['city']==city_code[city])&(diaDf['date']==now_date)]
                else:
                    df = pd.DataFrame([[city_code[city], now_date, 0, 0]],
                        columns = ['city', 'date', 'count', 'accumulateCount'])
                newDf = newDf.append(df)
        
        else:
            for city in city_code:
                df = pd.DataFrame([[city_code[city], now_date, 0, 0]],
                    columns = ['city', 'date', 'count', 'accumulateCount'])
                newDf = newDf.append(df) 

    # Fix Accumulate Count
    index = 0
    for city in city_code:
        count = 0
        cityDf = newDf[newDf['city']==city_code[city]]
        for i in range(cityDf.shape[0]):
            if cityDf.iloc[i].loc['accumulateCount'] == '0':
                newDf.iloc[index * n_city + i].loc['accumulateCount'] = count
            else:
                count = int(cityDf.iloc[i].loc['accumulateCount'])
        index += 1

    # Fix TW Value
    index = 1
    for i in range(n_date):
        now_date = str(start_date + datetime.timedelta(days=i)).split(' ')[0]
        dateDf = newDf[newDf['date']==now_date]
        count, accumulate_count = 0, 0
        for c in range(n_city-1):
            count += int(dateDf.iloc[c].loc['count'])
            accumulate_count += int(dateDf.iloc[c].loc['accumulateCount'])
        newDf.iloc[index * n_city - 1].loc['count'] = count
        newDf.iloc[index * n_city - 1].loc['accumulateCount'] = accumulate_count
        index += 1

    return newDf
    



if __name__=='__main__':
    diaDf = parseDiagnoseData('./diagnosed.csv')
    diaDf = addDate(diaDf)
    print(diaDf.shape[0])
    diaDf.to_csv('timeline_diagnosed.csv', index=False)  

