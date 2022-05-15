""""""
# from datetime import datetime
# from typing import List
#
# from mongoengine import (
#     Document,
#     DateTimeField,
#     FloatField,
#     StringField,
#     IntField,
#     connect,
#     QuerySet
# )
# from mongoengine.errors import DoesNotExist
#
# from vnpy.trader.constant import Exchange, Interval
# from vnpy.trader.object import BarData, TickData
# from vnpy.trader.database import (
#     BaseDatabase,
#     BarOverview,
#     DB_TZ,
#     convert_tz
# )
# from vnpy.trader.setting import SETTINGS
#
#
# class DbBarData(Document):
#     """"""
#
#     symbol: str = StringField()
#     exchange: str = StringField()
#     datetime: datetime = DateTimeField()
#     interval: str = StringField()
#
#     volume: float = FloatField()
#     open_interest: float = FloatField()
#     open_price: float = FloatField()
#     high_price: float = FloatField()
#     low_price: float = FloatField()
#     close_price: float = FloatField()
#
#     meta = {
#         "indexes": [
#             {
#                 "fields": ("symbol", "exchange", "interval", "datetime"),
#                 "unique": True,
#             }
#         ]
#     }
#
#
# class DbTickData(Document):
#     """"""
#
#     symbol: str = StringField()
#     exchange: str = StringField()
#     datetime: datetime = DateTimeField()
#
#     name: str = StringField()
#     volume: float = FloatField()
#     open_interest: float = FloatField()
#     last_price: float = FloatField()
#     last_volume: float = FloatField()
#     limit_up: float = FloatField()
#     limit_down: float = FloatField()
#
#     open_price: float = FloatField()
#     high_price: float = FloatField()
#     low_price: float = FloatField()
#     close_price: float = FloatField()
#     pre_close: float = FloatField()
#
#     bid_price_1: float = FloatField()
#     bid_price_2: float = FloatField()
#     bid_price_3: float = FloatField()
#     bid_price_4: float = FloatField()
#     bid_price_5: float = FloatField()
#
#     ask_price_1: float = FloatField()
#     ask_price_2: float = FloatField()
#     ask_price_3: float = FloatField()
#     ask_price_4: float = FloatField()
#     ask_price_5: float = FloatField()
#
#     bid_volume_1: float = FloatField()
#     bid_volume_2: float = FloatField()
#     bid_volume_3: float = FloatField()
#     bid_volume_4: float = FloatField()
#     bid_volume_5: float = FloatField()
#
#     ask_volume_1: float = FloatField()
#     ask_volume_2: float = FloatField()
#     ask_volume_3: float = FloatField()
#     ask_volume_4: float = FloatField()
#     ask_volume_5: float = FloatField()
#
#     meta = {
#         "indexes": [
#             {
#                 "fields": ("symbol", "exchange", "datetime"),
#                 "unique": True,
#             }
#         ],
#     }
#
#
# class DbBarOverview(Document):
#     """"""
#
#     symbol: str = StringField()
#     exchange: str = StringField()
#     interval: str = StringField()
#     count: int = IntField()
#     start: datetime = DateTimeField()
#     end: datetime = DateTimeField()
#
#     meta = {
#         "indexes": [
#             {
#                 "fields": ("symbol", "exchange", "interval"),
#                 "unique": True,
#             }
#         ],
#     }
#
#
# class MongodbDatabase(BaseDatabase):
#     """"""
#
#     def __init__(self) -> None:
#         """"""
#         database = SETTINGS["database.database"]
#         host = SETTINGS["database.host"]
#         port = SETTINGS["database.port"]
#         username = SETTINGS["database.user"]
#         password = SETTINGS["database.password"]
#         authentication_source = SETTINGS["database.authentication_source"]
#
#         if not username:
#             username = None
#             password = None
#             authentication_source = None
#
#         connect(
#             db=database,
#             host=host,
#             port=port,
#             username=username,
#             password=password,
#             authentication_source=authentication_source,
#         )
#
#     def save_bar_data(self, bars: List[BarData]) -> bool:
#         """"""
#         # Store key parameters
#         bar = bars[0]
#         symbol = bar.symbol
#         exchange = bar.exchange
#         interval = bar.interval
#
#         # Upsert data into mongodb
#         for bar in bars:
#             bar.datetime = convert_tz(bar.datetime)
#
#             d = bar.__dict__
#             d["exchange"] = d["exchange"].value
#             d["interval"] = d["interval"].value
#             d.pop("gateway_name")
#             d.pop("vt_symbol")
#             param = to_update_param(d)
#
#             DbBarData.objects(
#                 symbol=d["symbol"],
#                 exchange=d["exchange"],
#                 interval=d["interval"],
#                 datetime=d["datetime"],
#             ).update_one(upsert=True, **param)
#
#         # Update bar overview
#         try:
#             overview: DbBarOverview = DbBarOverview.objects(
#                 symbol=symbol,
#                 exchange=exchange.value,
#                 interval=interval.value
#             ).get()
#         except DoesNotExist:
#             overview: DbBarOverview = DbBarOverview(
#                 symbol=symbol,
#                 exchange=exchange.value,
#                 interval=interval.value
#             )
#
#         if not overview.start:
#             overview.start = bars[0].datetime
#             overview.end = bars[-1].datetime
#             overview.count = len(bars)
#         else:
#             overview.start = min(bars[0].datetime, overview.start)
#             overview.end = max(bars[-1].datetime, overview.end)
#             overview.count = DbBarData.objects(
#                 symbol=symbol,
#                 exchange=exchange.value,
#                 interval=interval.value
#             ).count()
#
#         overview.save()
#
#     def save_tick_data(self, ticks: List[TickData]) -> bool:
#         """"""
#         for tick in ticks:
#             tick.datetime = convert_tz(tick.datetime)
#
#             d = tick.__dict__
#             d["exchange"] = d["exchange"].value
#             d.pop("gateway_name")
#             d.pop("vt_symbol")
#             param = to_update_param(d)
#
#             DbTickData.objects(
#                 symbol=d["symbol"],
#                 exchange=d["exchange"],
#                 datetime=d["datetime"],
#             ).update_one(upsert=True, **param)
#
#     def load_bar_data(
#         self,
#         symbol: str,
#         exchange: Exchange,
#         interval: Interval,
#         start: datetime,
#         end: datetime
#     ) -> List[BarData]:
#         """"""
#         s: QuerySet = DbBarData.objects(
#             symbol=symbol,
#             exchange=exchange.value,
#             interval=interval.value,
#             datetime__gte=convert_tz(start),
#             datetime__lte=convert_tz(end),
#         )
#
#         vt_symbol = f"{symbol}.{exchange.value}"
#         bars: List[BarData] = []
#         for db_bar in s:
#             db_bar.datetime = DB_TZ.localize(db_bar.datetime)
#             db_bar.exchange = Exchange(db_bar.exchange)
#             db_bar.interval = Interval(db_bar.interval)
#             db_bar.gateway_name = "DB"
#             db_bar.vt_symbol = vt_symbol
#             bars.append(db_bar)
#
#         return bars
#
#     def load_tick_data(
#         self,
#         symbol: str,
#         exchange: Exchange,
#         start: datetime,
#         end: datetime
#     ) -> List[TickData]:
#         """"""
#         s: QuerySet = DbTickData.objects(
#             symbol=symbol,
#             exchange=exchange.value,
#             datetime__gte=convert_tz(start),
#             datetime__lte=convert_tz(end),
#         )
#
#         vt_symbol = f"{symbol}.{exchange.value}"
#         ticks: List[TickData] = []
#         for db_tick in s:
#             db_tick.datetime = DB_TZ.localize(db_tick.datetime)
#             db_tick.exchange = Exchange(db_tick.exchange)
#             db_tick.gateway_name = "DB"
#             db_tick.vt_symbol = vt_symbol
#             ticks.append(db_tick)
#
#         return ticks
#
#     def delete_bar_data(
#         self,
#         symbol: str,
#         exchange: Exchange,
#         interval: Interval
#     ) -> int:
#         """"""
#         count = DbBarData.objects(
#             symbol=symbol,
#             exchange=exchange.value,
#             interval=interval.value
#         ).delete()
#
#         # Delete bar overview
#         DbBarOverview.objects(
#             symbol=symbol,
#             exchange=exchange.value,
#             interval=interval.value
#         ).delete()
#
#         return count
#
#     def delete_tick_data(
#         self,
#         symbol: str,
#         exchange: Exchange
#     ) -> int:
#         """"""
#         count = DbTickData.objects(
#             symbol=symbol,
#             exchange=exchange.value
#         ).delete()
#         return count
#
#     def get_bar_overview(self) -> List[BarOverview]:
#         """
#         Return data avaible in database.
#         """
#         # Init bar overview for old version database
#         data_count = DbBarData.objects.count()
#         overview_count = DbBarOverview.objects.count()
#         if data_count and not overview_count:
#             self.init_bar_overview()
#
#         s: QuerySet = DbBarOverview.objects()
#         overviews = []
#         for overview in s:
#             overview.exchange = Exchange(overview.exchange)
#             overview.interval = Interval(overview.interval)
#             overviews.append(overview)
#         return overviews
#
#     def init_bar_overview(self) -> None:
#         """
#         Init overview table if not exists.
#         """
#         s: QuerySet = (
#             DbBarData.objects.aggregate({
#                 "$group": {
#                     "_id": {
#                         "symbol": "$symbol",
#                         "exchange": "$exchange",
#                         "interval": "$interval",
#                     },
#                     "count": {"$sum": 1}
#                 }
#             })
#         )
#
#         for d in s:
#             id_data = d["_id"]
#
#             overview = DbBarOverview()
#             overview.symbol = id_data["symbol"]
#             overview.exchange = id_data["exchange"]
#             overview.interval = id_data["interval"]
#             overview.count = d["count"]
#
#             start_bar: DbBarData = (
#                 DbBarData.objects(
#                     symbol=id_data["symbol"],
#                     exchange=id_data["exchange"],
#                     interval=id_data["interval"],
#                 )
#                 .order_by("+datetime")
#                 .first()
#             )
#             overview.start = start_bar.datetime
#
#             end_bar: DbBarData = (
#                 DbBarData.objects(
#                     symbol=id_data["symbol"],
#                     exchange=id_data["exchange"],
#                     interval=id_data["interval"],
#                 )
#                 .order_by("-datetime")
#                 .first()
#             )
#             overview.end = end_bar.datetime
#
#             overview.save()
#
#
# def to_update_param(d: dict) -> dict:
#     """
#     Convert data dict to update parameters.
#     """
#     param = {f"set__{k}": v for k, v in d.items()}
#     return param

from datetime import datetime
from typing import List

from pymongo import ASCENDING, MongoClient
from pymongo.database import Database
from pymongo.cursor import Cursor
from pymongo.collection import Collection
from pymongo.results import DeleteResult

from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.object import BarData, TickData
from vnpy.trader.database import BaseDatabase, BarOverview, DB_TZ
from vnpy.trader.setting import SETTINGS


class MongodbDatabase(BaseDatabase):
    """MongoDB数据库接口"""

    def __init__(self) -> None:
        """"""
        # 读取配置
        self.database: str = SETTINGS["database.database"]
        self.host: str = SETTINGS["database.host"]
        self.port: int = SETTINGS["database.port"]
        self.username: str = SETTINGS["database.user"]
        self.password: str = SETTINGS["database.password"]

        # 创建客户端
        if self.username and self.password:
            self.client: MongoClient = MongoClient(
                host=self.host,
                port=self.port,
                tz_aware=True,
                username=self.username,
                password=self.password,
                tzinfo=DB_TZ
            )
        else:
            self.client: MongoClient = MongoClient(
                host=self.host,
                port=self.port,
                tz_aware=True,
                tzinfo=DB_TZ
            )

        # 初始化数据库
        self.db: Database = self.client[self.database]

        # 初始化K线数据表
        self.bar_collection: Collection = self.db["bar_data"]
        self.bar_collection.create_index(
            [
                ("exchange", ASCENDING),
                ("symbol", ASCENDING),
                ("interval", ASCENDING),
                ("datetime", ASCENDING),
            ],
            unique=True
        )

        # 初始化Tick数据表
        self.tick_collection: Collection = self.db["tick_data"]
        self.tick_collection.create_index(
            [
                ("exchange", ASCENDING),
                ("symbol", ASCENDING),
                ("datetime", ASCENDING),
            ],
            unique=True
        )

        # 初始化K线概览表
        self.overview_collection: Collection = self.db["bar_overview"]
        self.overview_collection.create_index(
            [
                ("exchange", ASCENDING),
                ("symbol", ASCENDING),
                ("interval", ASCENDING),
            ],
            unique=True
        )

    def save_bar_data(self, bars: List[BarData]) -> bool:
        """保存K线数据"""
        for bar in bars:
            # 逐个插入
            filter = {
                "symbol": bar.symbol,
                "exchange": bar.exchange.value,
                "datetime": bar.datetime,
                "interval": bar.interval.value,
            }

            d = {
                "symbol": bar.symbol,
                "exchange": bar.exchange.value,
                "datetime": bar.datetime,
                "interval": bar.interval.value,
                "volume": bar.volume,
                "turnover": bar.turnover,
                "open_interest": bar.open_interest,
                "open_price": bar.open_price,
                "high_price": bar.high_price,
                "low_price": bar.low_price,
                "close_price": bar.close_price,
            }

            self.bar_collection.replace_one(filter, d, upsert=True)

        # 更新汇总
        filter = {
            "symbol": bar.symbol,
            "exchange": bar.exchange.value,
            "interval": bar.interval.value
        }

        overview = self.overview_collection.find_one(filter)

        if not overview:
            overview = {
                "symbol": bar.symbol,
                "exchange": bar.exchange.value,
                "interval": bar.interval.value,
                "count": len(bars),
                "start": bars[0].datetime,
                "end": bars[-1].datetime
            }
        else:
            overview["start"] = min(bars[0].datetime, overview["start"])
            overview["end"] = max(bars[-1].datetime, overview["end"])

            c: Cursor = self.bar_collection.find(filter)
            overview["count"] = c.count()

        self.overview_collection.update(filter, overview, upsert=True)

        return True

    def save_tick_data(self, ticks: List[TickData]) -> bool:
        """保存TICK数据"""
        for tick in ticks:
            filter = {
                "symbol": tick.symbol,
                "exchange": tick.exchange.value,
                "datetime": tick.datetime,
            }

            d = {
                "symbol": tick.symbol,
                "exchange": tick.exchange.value,
                "datetime": tick.datetime,
                "name": tick.name,
                "volume": tick.volume,
                "turnover": tick.turnover,
                "open_interest": tick.open_interest,
                "last_price": tick.last_price,
                "last_volume": tick.last_volume,
                "limit_up": tick.limit_up,
                "limit_down": tick.limit_down,
                "open_price": tick.open_price,
                "high_price": tick.high_price,
                "low_price": tick.low_price,
                "pre_close": tick.pre_close,
                "bid_price_1": tick.bid_price_1,
                "bid_price_2": tick.bid_price_2,
                "bid_price_3": tick.bid_price_3,
                "bid_price_4": tick.bid_price_4,
                "bid_price_5": tick.bid_price_5,
                "ask_price_1": tick.ask_price_1,
                "ask_price_2": tick.ask_price_2,
                "ask_price_3": tick.ask_price_3,
                "ask_price_4": tick.ask_price_4,
                "ask_price_5": tick.ask_price_5,
                "bid_volume_1": tick.bid_volume_1,
                "bid_volume_2": tick.bid_volume_2,
                "bid_volume_3": tick.bid_volume_3,
                "bid_volume_4": tick.bid_volume_4,
                "bid_volume_5": tick.bid_volume_5,
                "ask_volume_1": tick.ask_volume_1,
                "ask_volume_2": tick.ask_volume_2,
                "ask_volume_3": tick.ask_volume_3,
                "ask_volume_4": tick.ask_volume_4,
                "ask_volume_5": tick.ask_volume_5,
                "localtime": tick.localtime,
            }

            self.tick_collection.replace_one(filter, d, upsert=True)

        return True

    def load_bar_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval,
        start: datetime,
        end: datetime
    ) -> List[BarData]:
        """读取K线数据"""
        filter = {
            "symbol": symbol,
            "exchange": exchange.value,
            "interval": interval.value,
            "datetime": {
                "$gte": start,
                "$lte": end
            }
        }

        c: Cursor = self.bar_collection.find(filter)

        bars = []
        for d in c:
            d["exchange"] = Exchange(d["exchange"])
            d["interval"] = Interval(d["interval"])
            d["gateway_name"] = "DB"
            d.pop("_id")

            bar = BarData(**d)
            bars.append(bar)

        return bars

    def load_tick_data(
        self,
        symbol: str,
        exchange: Exchange,
        start: datetime,
        end: datetime
    ) -> List[TickData]:
        """读取TICK数据"""
        filter = {
            "symbol": symbol,
            "exchange": exchange.value,
            "datetime": {
                "$gte": start,
                "$lte": end
            }
        }

        c: Cursor = self.tick_collection.find(filter)

        ticks = []
        for d in c:
            d["exchange"] = Exchange(d["exchange"])
            d["gateway_name"] = "DB"
            d.pop("_id")

            tick = TickData(**d)
            ticks.append(tick)

        return ticks

    def delete_bar_data(
        self,
        symbol: str,
        exchange: Exchange,
        interval: Interval
    ) -> int:
        """删除K线数据"""
        filter = {
            "symbol": symbol,
            "exchange": exchange.value,
            "interval": interval.value,
        }

        result = self.bar_collection.delete_many(filter)
        self.overview_collection.delete_one(filter)

        return result.deleted_count

    def delete_tick_data(
        self,
        symbol: str,
        exchange: Exchange
    ) -> int:
        """删除TICK数据"""
        filter = {
            "symbol": symbol,
            "exchange": exchange.value
        }

        result: DeleteResult = self.tick_collection.delete_many(filter)
        return result.deleted_count

    def get_bar_overview(self) -> List[BarOverview]:
        """查询数据库中的K线汇总信息"""
        c: Cursor = self.overview_collection.find()

        overviews = []
        for d in c:
            d["exchange"] = Exchange(d["exchange"])
            d["interval"] = Interval(d["interval"])
            d.pop("_id")

            overview = BarOverview(**d)
            overviews.append(overview)

        return overviews

database_manager = MongodbDatabase()
