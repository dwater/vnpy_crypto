# 现货的
from time import sleep
from logging import INFO

from vnpy.app.cta_strategy import CtaStrategyApp, CtaEngine
from vnpy.app.cta_strategy.base import EVENT_CTA_LOG

from vnpy.event import EventEngine
from vnpy.gateway.binance import BinanceGateway
from vnpy.trader.engine import MainEngine
from vnpy.trader.setting import SETTINGS

SETTINGS["log.active"] = True
SETTINGS["log.level"] = INFO
# 打印信息到终端
SETTINGS["log.console"] = True

# 币安现货的
binance_settings = {
    "key": "xx",
    "secret": "xx",
    "session_number": 3,
    "proxy_host": "127.0.0.1",
    "proxy_port": 8001
}

# 币安期货的
binances_settings = {
    "key": "xx",
    "secret": "xx",
    "会话数": 3,
    "服务器": "TESTNET",
    "合约模式": "正向",
    "代理地址": "127.0.0.1",
    "代理端口": 8001
}

if __name__ == '__main__':
    SETTINGS["log.file"] = True

    # 初始化事件引擎
    event_engine = EventEngine()
    # 初始化主引擎
    main_engine = MainEngine(event_engine)
    # 加载币安现货的网关
    main_engine.add_gateway(BinanceGateway)
    # 加载币安合约的网关
    # main_engine.add_gateway(BinancesGateway)

    # 添加cta策略的app
    cta_engine: CtaEngine = main_engine.add_app(CtaStrategyApp)

    main_engine.write_log("主引擎创建成功")

    log_engine = main_engine.get_engine("log")
    event_engine.register(EVENT_CTA_LOG, log_engine.process_log_event)
    main_engine.write_log("注册日志事件监听")

    # 连接到交易所
    main_engine.connect(binance_settings, "BINANCE")
    main_engine.write_log("连接BINANCE 现货接口")

    # main_engine.connect(binances_settings, "BINANCES")
    # main_engine.write_log("连接BINANCE 合约接口")

    sleep(20)  # 稍作等待策略启动完成。

    cta_engine.init_engine()
    # 启动引擎 --> 实际上是处理CTA策略要准备的事情，加载策略
    # 具体加载的策略来自于配置文件howtrader/cta_strategy_settings.json
    # 仓位信息来自于howtrader/cta_strategy_data.json
    main_engine.write_log("CTA策略初始化完成")

    cta_engine.add_strategy('SpotGridAStrategy', 'spot_grid_a_strategy', 'bnbusdt.BINANCE', {})
    #  在配置文件有这个配置信息就不需要手动添加。
    cta_engine.init_all_strategies()  # 初始化所有的策略, 具体启动的哪些策略是来自于配置文件的

    sleep(30)  # 预留足够的时间让策略去初始化.

    main_engine.write_log("CTA策略全部初始化")

    cta_engine.start_all_strategies()  # 开启所有的策略.

    main_engine.write_log("CTA策略全部启动")

    while True:
        sleep(10)
