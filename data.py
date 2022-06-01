import csv
import json

# city code from https://zh.m.wikipedia.org/zh-tw/ISO_3166-2:TW
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

# vaccine data
# https://covid-19.nchc.org.tw/api.php?tableID=2006
# curl -o vaccineCityLevel.csv https://covid-19.nchc.org.tw/api/csv\?CK\=covid-19@nchc.org.tw\&querydata\=2006

timeDict = {}

with open("vaccineCityLevel.csv", encoding = "Big5") as csvfile:
    rows = csv.DictReader(csvfile)
    for row in rows:
        if row["群組"] == "總計":
            if row['發佈統計日期']  not in timeDict:
                timeDict[row['發佈統計日期']] = {}
            timeDict[row['發佈統計日期']][city_code[row['縣市']]] = {
                "vac_1": row["第1劑"],
                "vac_2": row["第2劑"],
                "vac_3": row["追加劑"],
                "vac_4": row["加強劑"]
            }

# print(json.dumps(timeDict, indent=2))

# diagnosed data
# https://covid-19.nchc.org.tw/api.php?tableID=5002
# curl -o diagnosedCityData.csv https://covid-19.nchc.org.tw/api/csv\?CK\=covid-19@nchc.org.tw\&querydata\=5002

# https://www.ris.gov.tw/app/portal/346



# output as timeline data. no one-hot
with open("timeline.csv", "w", newline="") as outfile:
    fieldnames = ['date', 'city', 'vac_1', 'vac_2', 'vac_3', 'vac_4']
    writer = csv.DictWriter(outfile, fieldnames)
    writer.writeheader()
    for date, cityDict in timeDict.items():
        for city, data in cityDict.items():
            writer.writerow({
                'date': date,
                'city': city,
                'vac_1': data['vac_1'],
                'vac_2': data['vac_2'],
                'vac_3': data['vac_3'],
                'vac_4': data['vac_4'],
            })