```
Userid: digitalassetcube
Password: VOly059Ba3IjPx0
keygen.id=693FB8-9183BF-67AE2F-4379DD-BA9A47-V3
keygen.accountId=c046d877-4753-4b77-9984-b618a5aed0fb
```

## docs

- [Reference Guide](https://doc.algotrader.com/html_single/index.html)
- [Python文档](https://doc.algotrader.com/pythondoc/index.htm)
- [Basics of Market Microstructure](https://www.youtube.com/watch?app=desktop&v=q9hJBfNjsnM)
- [tick与bar](https://cloud.tencent.com/developer/article/1457661)
- Python API
  - [策略class](https://doc.algotrader.com/pythondoc/services/strategy.html)
  - [PythonToAlgoTraderInterface class](https://doc.algotrader.com/pythondoc/interfaces/py2at.html#algotrader_com.interfaces.py2at.PythonToAlgoTraderInterface)
  - [Tick class](https://doc.algotrader.com/pythondoc/domain/market_data.html#algotrader_com.domain.market_data.Tick)
    - 🐛 there is no `adapter_type`, but `connector_descriptor`
  - [LimitOrder](https://doc.algotrader.com/pythondoc/domain/order.html#algotrader_com.domain.order.LimitOrder)
    - [Order Status](https://doc.algotrader.com/html_single/index.html#d0e9812)
  - [MarketSweepOrder](https://doc.algotrader.com/html_single/index.html#MarketSweepOrder) 看起来会放限价单, 没有执行则自动用市价
- Python语法
  - [Decimal](https://docs.python.org/zh-cn/3/library/decimal.html)
- 交易所
  - [Deribit的限制](https://doc.algotrader.com/html_single/index.html#d0e14456)
  - [FTX的限制](https://doc.algotrader.com/html_single/index.html#d0e15071)

|             | Derbit   | FTX      |
| ----------- | -------- | -------- |
| Symbol      | BTC25H22 | BTC25H22 |
| Account ID  | 57       | 11227    |
| Security ID | 14330    | 14330    |
| MinimumTick | 0.5      | 1        |

## Qs

- same security_id? [python strategy state](https://doc.algotrader.com/html_single/index.html#d0e2731)?

## 改动

```
-Dsimulation=true
-DstrategyName=TEST
-DdataSource.0.dataSourceType=DB
-DdataSource.0.eventType=TICK
-DdataSource.0.dataFilesDir=files
-DdataSource.0.barSize=MIN_5
-DdataSource.0.batchSize=2000
-Dspring.profiles.active=pythonIntegration,simulation,hybridDataSource,influxDB
-DdataSource.loadSampleData=true
-DoverridesPath="..\..\bootstrap\launch\configurationOverrides\config-overrides.json"
```

```
-DstrategyName=TEST
-Dmisc.embedded=true
-DdataSource.0.dataSourceType=DB
-DdataSource.0.eventType=TICK
-DdataSource.0.dataFilesDir=files
-DdataSource.0.barSize=MIN_5
-DdataSource.0.batchSize=2000
-Dspring.profiles.active=pythonIntegration,live,hybridDataSource,embeddedBroker,html5,influxDB
-DdataSource.loadSampleData=true
-DoverridesPath="..\..\bootstrap\launch\configurationOverrides\config-overrides.json"
```

**StragetyStarter-ems**的module