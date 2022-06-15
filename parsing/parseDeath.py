import requests
from bs4 import BeautifulSoup
import re
import csv
import json
import pandas as pd

base_url = "https://www.cdc.gov.tw"
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

city_dict = {}

def getDeathNum(total_num, text, city_dict2):
    if not total_num:
        for city_name, city_code in city_codes.items():
            city_dict2[city_code].append(city_dict2[city_code][-1])
        return

    for city_name, city_code in city_codes.items():
        city_search = re.search(rf'{city_name}[^\d,]*([\d,]+)', text)
        if city_search:
            death_accum = int(city_search.group(1).replace(",", ""))
        else:
            death_accum = 0
        city_dict2[city_code].append(death_accum)
    city_dict2[city_code][-1] = total_num


def getDeathData(date_list):
    city_dict2 = {}
    for city_code in city_codes.values():
        city_dict2[city_code] = []
    date_index = len(date_list) - 1

    searchStop = False

    for page in range(1,11):
        news = requests.get(f"https://www.cdc.gov.tw/Bulletin/List/MmgtpeidAR5Ooai4-fgHzQ?page={page}&keyword=%27COVID-19%E7%A2%BA%E5%AE%9A%E7%97%85%E4%BE%8B%EF%BC%8C%E5%88%86%E5%88%A5%E7%82%BA%27")

        news_soup = BeautifulSoup(news.text, "html.parser")
        titles = news_soup.select("p.JQdotdotdot")
        for title in titles:
            link = title.find_parent("a").get("href")
            # print(base_url + link)
            news_content = requests.get(base_url + link)
            
            content_soup = BeautifulSoup(news_content.text, "html.parser")
            content_text = content_soup.select_one("div.news-v3-in > div")
            date = content_text.select_one("div.text-right").text[5:]
            print(date)

            m = re.search(r'累計[\d,]+例COVID-19死亡病例，其中([\d,]+)[\ ]?例本土，個案居住縣市分布為([^；]+)；',
                            content_text.text)
            if m:
                print(m.group(1), m.group(2))
                while date_index >= 0 and date_list[date_index] != date:
                    getDeathNum(None, None, city_dict2)
                    date_index -= 1
                if date_index >= 0:
                    getDeathNum(int(m.group(1).replace(",", "")), m.group(2), city_dict2)
                    date_index -= 1

                if date_index < 0:
                    searchStop = True
                    break
            print("----")

        if searchStop:
            break

    date_len = len(date_list)
    for city, city_data in city_dict2.items():
        if city not in city_dict:
            city_dict[city] = {}
        for i in range(date_len):
            city_dict[city][date_list[i]] = {
                "death_accum": city_data[-i-1],
            }
            try:
                city_dict[city][date_list[i]]["death_new"] = city_data[date_len-1-i] - city_data[date_len-i]
            except:
                city_dict[city][date_list[i]]["death_new"] = 0

# output as timeline data. no one-hot
def writeFile():
    with open("timeline_death.csv", "w", newline="") as outfile:
        fieldnames = ['city', 'date', 'death_new', 'death_accum']
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()
        for city, time_dict in city_dict.items():
            for date, data in time_dict.items():
                writer.writerow({
                    'city': city,
                    'date': date,
                    'death_new': data['death_new'],
                    'death_accum': data['death_accum'],
                })


if __name__ == '__main__':
    date_list = pd.date_range(start="2022-03-10", end="2022-06-04", freq='D').strftime("%Y-%m-%d").tolist()
    getDeathData(date_list)

    print(json.dumps(city_dict, indent=2))

    writeFile()