# AI2022-Final Project
COVID-19 Infected Prediction.

## How to Get Raw Data
* daily new infected cases
    ```
    curl -o infected.csv https://covid-19.nchc.org.tw/api/csv?CK=covid-19@nchc.org.tw&querydata=5002
    ```
* daily dead cases
* population
* age distribution
* longitude and latitude

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
