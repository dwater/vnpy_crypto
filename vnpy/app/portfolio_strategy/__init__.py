from pathlib import Path

from vnpy.trader.app import BaseApp
from .backtesting import BacktestingEngine
from .base import APP_NAME
from .engine import StrategyEngine
from .template import StrategyTemplate


class PortfolioStrategyApp(BaseApp):
    """"""

    app_name = APP_NAME
    app_module = __module__
    app_path = Path(__file__).parent
    display_name = "组合策略"
    engine_class = StrategyEngine
    widget_name = "PortfolioStrategyManager"
    icon_name = "strategy.ico"
