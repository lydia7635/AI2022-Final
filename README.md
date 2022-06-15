# AI2022-Final Project
COVID-19 Infected Prediction.

## How to Get Raw Data
在 `parsing` 資料夾中進行以下動作：
* daily new infected cases
    1. 下載 raw data
        ```
        curl -o diagnosed.csv https://covid-19.nchc.org.tw/api/csv?CK=covid-19@nchc.org.tw&querydata=5002
        ```
    2. 使用 Python script 整理
        ```
        python3 parseInfected.py
        ```
    3. 產生的 `timeline_diagnosed.csv` 放入 `../data` 資料夾中
* daily dead cases
    1. 使用 Python script 抓取新聞稿資料並整理
        ```
        python3 parseDeath.py
        ```
        * 注意：可能因未來新聞稿格式更改而無法使用
    2. 產生的 `timeline_death.csv` 放入 `../data` 資料夾中
* population
    1. 從 https://www.ris.gov.tw/app/portal/346 下載 02縣市人口性比例及人口密度(9701) 檔案（111 年 4 月份）
    2. 將該檔案的 02-縣市別 工作表另存為 `population.csv`
    3. 使用 Python script 整理
        ```
        python3 populationPreproc.py
        ```
    4. 產生的 `populationAdj.csv` 放入 `../data` 資料夾中，並改名為 `population.csv`
* age distribution
    1. 從 https://www.ris.gov.tw/app/portal/346 下載 04縣市人口按單齡(9701) 檔案（111 年 4 月份），並更名為 `age.xls`
    2. 使用 Python script 整理
        ```
        python3 parseAge.py
        ```
    3. 產生的 `age.csv` 放入 `../data` 資料夾中
* longitude and latitude
    1. 參考 https://byronhu.wordpress.com/2013/09/09/台灣縣市經緯度/ ，並手動存成 `latitude.csv` 放入 `../data` 資料夾中

## How to make prediction with SIRD/LSTM?
* SIRD: Jupyter notebook `ai/AI2022_SIRD.ipynb`
* LSTM: Jupyter notebook `ai/AI2022_LSTM.ipynb`
* multivariate LSTM: Jupyter notebook `ai/AI2022_LSTM_multivariate.ipynb`
* LSTM with static data: Jupyter notebook `ai/AI2022_LSTM_static.ipynb`
* 將以上所有 model 的 long-term prediction 比較並作圖: `ai/AI2022_all.ipynb`

## File Structure
```
.
|____data/
| |____csv file ...
|____output/
| |____results of long-term prediction
|____parsing/
| |____scripts for parsing data
|____ai/
  |____Jupyter notebooks for model training and testing
```

## Note
* 移除 requirements.txt