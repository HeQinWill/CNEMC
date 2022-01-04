##  [CNEMC](http://106.37.208.233:20035/) 
从中国环境总站采集空气质量六参数（逐小时更新）  
数据发布说明里需注意的地方  
>- 监测点位1小时浓度平均值指该点位1小时内所测项目浓度的算术平均值或测量值，如16时的小时均值为15：00-16:00的算术平均值或测量值。
> - 8小时滑动平均值是指当前小时前8小时内所测项目小时浓度的算术平均值。
> - 发布结果通常为每小时更新1次，由于数据传输需要一定的时间，发布的数据约有半小时延滞，例如15时的监测数据在15:30左右发布。
### 本地部署
- 获取原始 wcf 格式的文件
```sh
/usr/bin/wget "https://air.cnemc.cn:18007/emcpublish/ClientBin/Env-CnemcPublish-RiaServices-EnvCnemcPublishDomainService.svc/binary/GetAQIDataPublishLives" -O /home/yourName/cnemc_$(date +%Y%m%d%H%M)
```

- 设置定时任务
```sh
13,43 * * * * /usr/bin/bash /home/yourName/cnemc.sh
```

- [定期转为 wcf 数据为 csv 并归档](https://github.com/HeQinWill/CNEMC/blob/main/conWCFarcCSV.ipynb)
---