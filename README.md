##  [CNEMC](http://106.37.208.233:20035/) 
从中国环境总站采集空气质量六参数（逐小时更新）

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