import pandas as pd

city_code = {
    "基隆市": "KEE",
    "新北市": "NWT",
    "臺北市": "TPE",
    "桃園市": "TAO",
    "新竹市": "HSZ",
    "新竹縣": "HSQ",
    "苗栗縣": "MIA",
    "臺中市": "TXG",
    "彰化縣": "CHA",
    "南投縣": "NAN",
    "雲林縣": "YUN",
    "嘉義縣": "CYQ",
    "嘉義市": "CYI",
    "臺南市": "TNN",
    "高雄市": "KHH",
    "屏東縣": "PIF",
    "宜蘭縣": "ILA",
    "花蓮縣": "HUA",
    "臺東縣": "TTT",
    "澎湖縣": "PEN",
    "金門縣": "KIN",
    "連江縣": "LIE",
    "全國": "TW"
}

def parsePopulationData(filePath):
    popDf=pd.read_csv(
        filePath, 
        skiprows=lambda x: x in [0,1,3],
        nrows=25, 
        usecols=range(12), 
        thousands=','
    )
    popDf.columns=[
        'Region', 'area', 'numCity', 'numVillage', 'numNeighborhood', 'numHouse',
        'population', 'male', 'female', 'sexRatio', 'densityArea', 'densityHouse'
    ]

    # Rename region in city codes
    popDf.loc[0, 'Region']='全國'
    popDf = popDf[popDf['Region']!='臺灣省']
    popDf = popDf[popDf['Region']!='福建省']
    popDf.loc[:, 'Region'] = popDf['Region'].map(lambda x: city_code[x])
    return popDf

if __name__=='__main__':
    df = parsePopulationData('./population.csv')
    print(df['sexRatio'])
    print(df)