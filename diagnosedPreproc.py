import pandas as pd

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
    diaDf = pd.read_csv(filename)
    diaDf.columns=[
            'index', 'guessDate', 'date', 'city', 'section', 'count', 'accumulateCount'   ]

        
    diaDf = diaDf[diaDf['section']=='全區']
    diaDf = diaDf[diaDf['city']!='境外移入']

    diaDf.reset_index(inplace = True)

    diaDf = diaDf[['date', 'city', 'count', 'accumulateCount']]

    # Rename city
    diaDf.loc[:, 'city'] = diaDf['city'].map(lambda x: city_code[x])

    return diaDf

if __name__=='__main__':
    diaDf = parseDiagnoseData('./diagnosed.csv')
    print(diaDf)
