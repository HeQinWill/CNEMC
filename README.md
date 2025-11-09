##  [CNEMC](https://air.cnemc.cn:18007) 
从中国环境总站采集空气质量六参数（逐小时更新）  
数据发布说明里需注意的地方  
> - 监测点位1小时浓度平均值指该点位1小时内所测项目浓度的算术平均值或测量值，如16时的小时均值为15:00-16:00的算术平均值或测量值。
> - 8小时滑动平均值是指当前小时前8小时内所测项目小时浓度的算术平均值。
> - 发布结果通常为每小时更新1次，由于数据传输需要一定的时间，发布的数据约有半小时延滞，例如15时的监测数据在15:30左右发布。

有关滑动均值的结果务必自己检核，发布时刻前面的数据有缺值时会带来误差！  

貌似新的数据不反也不提供 o3_24h 结果了，使用时请自己一并检查到底是哪个量（尤其是 2023-11-09 前和 2023-11-14 后）  
~抓取的文件中关于**臭氧**数据里 1 小时和 24 小时两列的位置放颠倒了，这里 csv 并未修改，使用时请按照下面的正确定义：~
- `o3_24h`: 最近 1 小时浓度均值
- `o3`: 最近 24 小时中 1 小时浓度均值的最大值
- `o3_8h_24h`: 自然日内（T1-T0/24）最近 8 小时滑动平均浓度，对于 T1-Tt (t<8) 则为这 t 个小时均值，所以只用 T8-T0/24 的结果
- `o3_8h`: 自然日内所有 8 小时滑动平均浓度中的最大值，所以只需看该日 T0/24  

对于其他五参数，`x`代表最近 1 小时浓度均值，`x_24`代表最近 24 小时中 1 小时浓度均值的均值。


官网现在还提供了一份 GeoJSON 的底图文件供使用: https://air.cnemc.cn:18007/Content/Scripts/Map/China.json

### 本地部署
- 获取返回的 JSON 格式站点观测结果（现在需要使用 post 方式）
```sh
/usr/bin/wget "https://air.cnemc.cn:18007/HourChangesPublish/GetAllAQIPublishLive" --no-check-certificate --post-data='' -O /home/opc/cnemc/cnemc_$(date +%Y%m%d%H%M).json
```
或者
```sh
curl -k 'https://air.cnemc.cn:18007/HourChangesPublish/GetAllAQIPublishLive' \
  -X 'POST' \
  -H 'Accept: */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 0' \
  -H 'Origin: https://air.cnemc.cn:18007' \
  -H 'Referer: https://air.cnemc.cn:18007/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'sec-ch-ua: "Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"' \
  -o cnemc_$(date +%Y%m%d%H%M).json
```

- 获取近24小时的数据
> 感谢 [@StorywithLove](https://github.com/HeQinWill/CNEMC/issues/3) 提醒这个接口，可一定程度填补缺失数据，具体修改请见 Commit [8ed9bb1](https://github.com/HeQinWill/CNEMC/commit/8ed9bb15768d1a070a694c568d2fa53e4f7bd249) 和 [18182df](https://github.com/HeQinWill/CNEMC/commit/18182dfc206f14a0dd4680bfac5b0de258d9ae25)
```sh
curl 'https://air.cnemc.cn:18007/HourChangesPublish/GetAQIHistoryByConditionHis' \
  -X 'POST' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Accept: */*' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Accept-Language: zh-CN,zh-Hans;q=0.9' \
  -H 'Accept-Encoding: gzip, deflate, br' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Origin: https://air.cnemc.cn:18007' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15' \
  -H 'Content-Length: 28' \
  -H 'Referer: https://air.cnemc.cn:18007/' \
  -H 'Connection: keep-alive' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'Priority: u=3, i' \
  --data 'date=2025-11-08+10%3A00%3A00' \
  -o cnemc_his_$(date +%Y%m%d%H%M).json
```

- 设置定时任务
```sh
13,43 * * * * /usr/bin/bash /home/yourName/cnemc.sh
```

- ~[定期转为 wcf 数据为 csv 并归档](https://github.com/HeQinWill/CNEMC/blob/main/conWCFarcCSV.ipynb)~  现在接口直接返回的是 JSON 格式数据，无需使用 wcf 工具解析
---
### 数据问题记录
- 2022-03-07T11.csv中 `1742A 阳泉市平坦` 站点，`so2_24h` 爬取的记录原先为 `28`，之后为 `20`，最终选择了 `20`  
其原因是该站在 `2022-03-07 01:00:00` 的 `so2` 突然升高到 `202`，后来该记录可能在统计时被剔除  
虽然相应的 csv 文件中仍然保留着 `T01` 的爬取结果，但此处建议不要使用 `202` 这条记录
- `1760A 沈抚新城` 站点从 `2022-05-31 16:00:00` 才有数据，所以对应的 `_24h` 都是那个时刻的，除了 `pm10` 是从前一个时刻就有

#### 未发布数据
- 2022-03-16 20:00:00
- 2022-05-03 02:00:00
- 2022-05-11 01:00:00
- 2022-05-31 08:00:00
- 2022-06-05 14:00:00
- 2022-06-07 23:00:00
- 2022-06-12 12:00:00
- 2022-06-12 22:00:00
- 2022-06-12 23:00:00
- 2022-06-13 00:00:00
- 2022-06-13 01:00:00
- 2022-06-13 02:00:00
- 2022-06-13 03:00:00
- 2022-06-13 04:00:00
- 2022-06-13 05:00:00
- 2022-06-13 06:00:00
- 2022-06-13 07:00:00
- 2022-06-13 08:00:00

#### 爬取遗漏
- 2022-03-28 09:00:00
- 2022-03-31 09:00:00
- 2022-05-17 09:00:00
- 2022-05-18 09:00:00
- 2022-05-19 09:00:00
- 2022-05-20 09:00:00
- 2022-05-21 09:00:00
- 2022-05-22 09:00:00
- 2022-05-23 09:00:00
- 2022-05-24 09:00:00
- 2022-05-25 09:00:00
- 2022-05-26 09:00:00
- 2022-05-27 09:00:00
- 2022-05-28 09:00:00
- 2022-05-29 09:00:00
- 2022-05-30 09:00:00
- 2022-05-30 10:00:00
- 2022-05-31 09:00:00
- 2022-06-01 09:00:00
- 2022-06-01 10:00:00
- 2022-06-01 19:00:00
- 2022-06-02 09:00:00
- 2022-06-02 10:00:00
- 2022-06-03 09:00:00
- 2022-06-04 09:00:00
- 2022-06-05 09:00:00

#### 其他渠道
https://quotsoft.net/air/
