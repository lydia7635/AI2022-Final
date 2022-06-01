import requests
from bs4 import BeautifulSoup
import re

base_url = "https://www.cdc.gov.tw"
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



def getDeathNum(text):
    dayDeath = {}


for page in range(1,2):
    news = requests.get(f"https://www.cdc.gov.tw/Bulletin/List/MmgtpeidAR5Ooai4-fgHzQ?page={page}&keyword=%27COVID-19%E7%A2%BA%E5%AE%9A%E7%97%85%E4%BE%8B%EF%BC%8C%E5%88%86%E5%88%A5%E7%82%BA%27")

    news_soup = BeautifulSoup(news.text, "html.parser")
    titles = news_soup.select("p.JQdotdotdot")
    for title in titles:
        link = title.find_parent("a").get("href")
        # print(base_url + link)
        news_content = requests.get(base_url + link)
        
        content_soup = BeautifulSoup(news_content.text, "html.parser")
        content_text = content_soup.select_one("div.news-v3-in > div")
        print(content_text.select_one("div.text-right").text[5:])


        # print(type(content_text.text))
        m = re.search(r'累計[\d,]+例COVID-19死亡病例，其中([\d,]+)例本土，個案居住縣市分布為([^；]+)；',
                        content_text.text)
        if m:
            print(m.group(1), m.group(2))

        print("----")