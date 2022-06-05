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

def printDF(city_list, age_list):
    city = {'city':city_list}
    ageDf = pd.DataFrame(city)
    
    N = len(age_list)
    M = len(age_list[0])
    
    for j in range(M):
        column = str(j * 5)
        tmp_list = []
        for i in range(N):
            tmp_list.append(age_list[i][j])
        ageDf[column] = tmp_list
    
    ageDf = ageDf[ageDf['city']!='臺灣省']
    ageDf = ageDf[ageDf['city']!='福建省']

    ageDf.loc[:, 'city'] = ageDf['city'].map(lambda x: city_code[x])

    ageDf.to_csv('age.csv', index=False)  

if __name__=='__main__':
    ageDf = pd.read_excel('age.xls')
    city_list = []
    age_list = []
    N, M = ageDf.shape[0], ageDf.shape[1]
    i = 7
    while i < N:
        city_list.append(ageDf.iloc[i, 0])
        j = 3
        this_age_list = []
        while j < M:
            this_age_list.append(ageDf.iloc[i-1, j])
            j += 6
        age_list.append(this_age_list)
        i += 3

    printDF(city_list, age_list)

