# -*- coding: utf8 -*-
import requests
import json
import pandas as pd
import numpy as np
from pathlib import Path
requests.packages.urllib3.disable_warnings()

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Origin': 'https://air.cnemc.cn:18007',
    'Referer': 'https://air.cnemc.cn:18007/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
}

if __name__ == "__main__":
    # 从API请求数据
    r = requests.post('https://air.cnemc.cn:18007/HourChangesPublish/GetAllAQIPublishLive', headers=headers, verify=False)

    # 解析得到的 json 数据
    data_dict = json.loads(r.content)

    # 将字典转为 DataFrame
    df = pd.DataFrame.from_dict(data_dict)
    
    # 对应原来输出的文件格式
    df.columns = df.columns.map(str.lower)
    df['timepoint'] = df['timepointstr'].str.replace('年', '-')\
                                        .str.replace('月', '-')\
                                        .str.replace('日 ', 'T')\
                                        .str.replace('时', '00')
    
    # 如果出现不同的时间就把全部数据输出一份
    if len(df['timepoint'].unique()) > 1:
        for t in range(len(df['timepoint'].unique())):
            timestamp = df['timepoint'].unique()[t][:13]
            daily_folder = Path('Error')/timestamp[:10]
            daily_folder.mkdir(parents=True, exist_ok=True)
            df.to_csv(daily_folder/(timestamp+'.csv'), index=None)

    # 将数据处理下再输出
    df_ = df[['timepoint', 'stationcode', 'longitude', 'latitude',
              'area', 'positionname', 'primarypollutant', 'aqi',
              'pm10', 'pm10_24h', 'pm2_5', 'pm2_5_24h',
              'o3', 'o3_24h', 'o3_8h', 'o3_8h_24h',
              'no2', 'no2_24h', 'so2', 'so2_24h',
              'co', 'co_24h']]
    df_ = df_.where(df != '—', np.nan)

    # 将每小时数据保存为 csv 文件
    timestamp = df['timepoint'].unique()[-1][:13]
    daily_folder = Path('Archive')/timestamp[:10]
    daily_folder.mkdir(parents=True, exist_ok=True)
    # 如果已经有过该文件只需要追加此刻获取的即可
    if (daily_folder/(timestamp+'.csv')).exists():
        df_.to_csv(daily_folder/(timestamp+'.csv'),
                   index=None, mode='a', header=False)
    else:
        df_.to_csv(daily_folder/(timestamp+'.csv'),
                   index=None, mode='w')
