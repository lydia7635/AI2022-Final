import csv
import json
import pandas as pd

# city code from https://zh.m.wikipedia.org/zh-tw/ISO_3166-2:TW
city_codes = {
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

cityDict = {}


# vaccine data
# https://covid-19.nchc.org.tw/api.php?tableID=2006
# curl -o vaccineCityLevel.csv https://covid-19.nchc.org.tw/api/csv\?CK\=covid-19@nchc.org.tw\&querydata\=2006
def getVaccineData():
    vaccineData = {
        "date": [],
        "city": [],
        "vac_1": [],
        "vac_2": [],
        "vac_3": [],
        "vac_4": [],
    }

    with open("vaccineCityLevel.csv", encoding = "Big5") as vaccineFile:
        rows = csv.DictReader(vaccineFile)
        for row in rows:
            if row["群組"] == "總計":
                vaccineData["date"].append(row["發佈統計日期"])
                vaccineData["city"].append(city_codes[row["縣市"]])
                vaccineData["vac_1"].append(row["第1劑"])
                vaccineData["vac_2"].append(row["第2劑"])
                vaccineData["vac_3"].append(row["追加劑"])
                vaccineData["vac_4"].append(row["加強劑"])
        vaccineData = pd.DataFrame(vaccineData)
        vaccineData['date'] = pd.to_datetime(vaccineData['date'])
        vaccineData = (vaccineData.set_index('date')
                        .groupby('city')[['vac_1', 'vac_2', 'vac_3', 'vac_4']]
                        .resample('d')
                        .ffill()
                        .reset_index())
        # print(vaccineData)

        for _, row in vaccineData.iterrows():
            city = row['city']
            date = row['date'].strftime('%Y-%m-%d')
            if city not in cityDict:
                cityDict[city] = {}
            cityDict[city][date] = {
                "vac_1": row["vac_1"],
                "vac_2": row["vac_2"],
                "vac_3": row["vac_3"],
                "vac_4": row["vac_4"]
            }

# diagnosed data
# https://covid-19.nchc.org.tw/api.php?tableID=5002
# curl -o diagnosedCityData.csv https://covid-19.nchc.org.tw/api/csv\?CK\=covid-19@nchc.org.tw\&querydata\=5002
def getDiagnosedData():
    pass

def getDeathData():
    pass


# https://www.ris.gov.tw/app/portal/346



# output as timeline data. no one-hot
def writeFile():
    with open("timeline.csv", "w", newline="") as outfile:
        fieldnames = ['city', 'date', 'vac_1', 'vac_2', 'vac_3', 'vac_4']
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()
        for city, timeDict in cityDict.items():
            for date, data in timeDict.items():
                writer.writerow({
                    'city': city,
                    'date': date,
                    'vac_1': data['vac_1'],
                    'vac_2': data['vac_2'],
                    'vac_3': data['vac_3'],
                    'vac_4': data['vac_4'],
                })


if __name__ == '__main__':
    getVaccineData()
    getDiagnosedData()
    getDeathData()
    # print(json.dumps(cityDict, indent=2))
    writeFile()
