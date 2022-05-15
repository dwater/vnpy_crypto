from vnpy.event import EventEngine

from vnpy.trader.engine import MainEngine
from vnpy.trader.ui import MainWindow, create_qapp

from vnpy.gateway.binance import BinanceSpotGateway
from vnpy.gateway.binance import BinanceUsdtGateway
from vnpy.gateway.binance import BinanceInverseGateway

from vnpy.app.cta_strategy import CtaStrategyApp  # CTA策略
from vnpy.app.data_manager import DataManagerApp  # 数据管理, csv_data
from vnpy.app.data_recorder import DataRecorderApp  # 录行情数据
from vnpy.app.algo_trading import AlgoTradingApp  # 算法交易
from vnpy.app.cta_backtester import CtaBacktesterApp  # 回测研究
from vnpy.app.risk_manager import RiskManagerApp  # 风控管理
from vnpy.app.spread_trading import SpreadTradingApp  # 价差交易
from vnpy.app.portfolio_strategy import PortfolioStrategyApp  # 组合策略

if __name__ == '__main__':
    qapp = create_qapp()

    event_engine = EventEngine()

    main_engine = MainEngine(event_engine)

    """
    币安的接口有现货和合约接口之分。 他们之间的区别是通过交易对来区分的。现货用小写，合约用大写。 
    * btcusdt.BINANCE 是现货的symbol
    * BTCUSDT.BINANCE合约的交易对
    * BTCUSD.BINANCE是合约的币本位保证金的交易对
    """

    # 币安现货
    main_engine.add_gateway(BinanceSpotGateway)
    # 币安正向合约
    main_engine.add_gateway(BinanceUsdtGateway)
    # 币安反向合约
    main_engine.add_gateway(BinanceInverseGateway)

    # bitmex
    # main_engine.add_gateway(BitmexGateway)

    # 策略
    main_engine.add_app(CtaStrategyApp)
    # 回测
    main_engine.add_app(CtaBacktesterApp)
    # 数据
    main_engine.add_app(DataManagerApp)
    # 算法交易
    main_engine.add_app(AlgoTradingApp)
    # 数据记录
    main_engine.add_app(DataRecorderApp)
    # 风险控制
    main_engine.add_app(RiskManagerApp)
    # 价差交易
    main_engine.add_app(SpreadTradingApp)
    # 期权交易
    # main_engine.add_app(OptionMasterApp)
    # 组合策略
    main_engine.add_app(PortfolioStrategyApp)

    main_window = MainWindow(main_engine, event_engine)

    main_window.show()

    qapp.exec()
