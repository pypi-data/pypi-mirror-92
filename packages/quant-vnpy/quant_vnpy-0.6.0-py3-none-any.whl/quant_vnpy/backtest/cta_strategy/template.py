"""
@author  : MG
@Time    : 2020/11/16 10:20
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
from datetime import datetime
from typing import Optional

import pandas as pd
from ibats_utils.mess import datetime_2_str, date_2_str
from vnpy.app.cta_strategy import CtaTemplate as CtaTemplateBase, TargetPosTemplate as TargetPosTemplateBase
from vnpy.trader.constant import Offset, Direction
from vnpy.trader.object import OrderData, BarData, TickData, TradeData

from quant_vnpy.backtest.commons import get_output_file_path
from quant_vnpy.config import logging
from quant_vnpy.db.orm import AccountStrategyStatusEnum
from quant_vnpy.report.collector import trade_data_collector, order_data_collector, latest_price_collector
from quant_vnpy.report.monitor import AccountStrategyStatusMonitor
from quant_vnpy.utils.enhancement import BarGenerator


class CtaTemplate(CtaTemplateBase):
    # 该标识位默认为0（关闭状态）。为1时开启，程序一旦平仓后则停止后续交易。该标识位用于在切换合约时使用
    stop_opening_pos = 0

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.parameters.append("stop_opening_pos")  # 增加 stop_opening_pos 用于合约切换是关闭当前线程
        self.logger = logging.getLogger(strategy_name)
        self.send_order_list = []  # 记录所有订单数据
        # 仅用于 on_order 函数记录上一个 order 使用，解决vnpy框架重复发送order的问题
        self._last_order = None
        self._trades = []  # 记录所有成交数据
        self.current_bar: Optional[BarData] = None
        self.bar_count = 0
        self.bg = BarGenerator(self.on_bar)
        # 是否实盘环境
        self._is_realtime_mode = self.strategy_name is not None and self.strategy_name != self.__class__.__name__
        self._strategy_status = AccountStrategyStatusEnum.Created
        # 最近一次下单的时间
        self.last_order_dt: Optional[datetime] = None
        # 是否收集申请单以及交易单记录
        self.enable_collect_data = self._is_realtime_mode
        if "enable_collect_data" in setting:
            self.enable_collect_data |= setting['enable_collect_data']

        if self.enable_collect_data:
            trade_data_collector.queue_timeout = 90 if self._is_realtime_mode else 1
            order_data_collector.queue_timeout = 90 if self._is_realtime_mode else 1

        if self._is_realtime_mode:
            self._strategy_status_monitor = AccountStrategyStatusMonitor(
                self.strategy_name,
                self._get_strategy_status,
                self._set_strategy_status,
                self.vt_symbol,
                setting
            )
            self._lock = self._strategy_status_monitor.lock
        else:
            self._strategy_status_monitor = None
            self._lock = None

    def _set_strategy_status(self, status: AccountStrategyStatusEnum):
        if not self._is_realtime_mode:
            # 仅针对实时交易是使用
            return
        if self._strategy_status == status:
            return

        if status == AccountStrategyStatusEnum.RunPending and self._strategy_status not in (
                AccountStrategyStatusEnum.Created, AccountStrategyStatusEnum.Running
        ):
            # AccountStrategyStatusEnum.RunPending 状态只从数据库端发起
            if self._lock is not None:
                self._lock.acquire()

            try:
                # 保险起见，为防止出现死循环调用，在 on_start 先把状态调整过来
                self._strategy_status = status
                self.write_log(f"策略 {self.strategy_name}[{self.vt_symbol}] 状态 "
                               f"{self._strategy_status.name} -> {status.name} 被远程启动")
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_start()

        elif status == AccountStrategyStatusEnum.StopPending and self._strategy_status == AccountStrategyStatusEnum.Running:
            # AccountStrategyStatusEnum.StopPending 状态只从数据库端发起
            if self._lock is not None:
                self._lock.acquire()

            try:
                # 保险起见，为防止出现死循环调用，在 on_stop 先把状态调整过来
                self._strategy_status = status
                self.write_log(f"策略 {self.strategy_name}[{self.vt_symbol}] 状态 "
                               f"{self._strategy_status.name} -> {status.name} 被远程停止")
            finally:
                if self._lock is not None:
                    self._lock.release()

            self.on_stop()
        else:
            self.write_log(f"策略 {self.strategy_name}[{self.vt_symbol}] 状态 "
                           f"{self._strategy_status.name} -> {status.name}")
            self._strategy_status = status

    def _get_strategy_status(self) -> AccountStrategyStatusEnum:
        return self._strategy_status

    def on_init(self) -> None:
        super().on_init()
        self.bar_count = 0
        self._set_strategy_status(AccountStrategyStatusEnum.Initialized)
        if self._strategy_status_monitor is not None and not self._strategy_status_monitor.is_alive():
            self._strategy_status_monitor.start()

    def on_start(self) -> None:
        super().on_start()
        self._set_strategy_status(AccountStrategyStatusEnum.Running)
        # 整理持仓信息
        self.write_log(f"策略启动，当前初始持仓： {self.vt_symbol} {self.pos}")
        self.put_event()
        # if self._is_realtime_mode:
        #     start_strategy_position_monitor()

    def on_tick(self, tick: TickData):
        super().on_tick(tick)
        # 激活分钟线 on_bar
        self.bg.update_tick(tick)
        latest_price_collector.put_nowait(tick)

    def on_bar(self, bar: BarData):
        super().on_bar(bar)
        self.current_bar: BarData = bar
        self.bar_count += 1

    def send_order(
            self,
            direction: Direction,
            offset: Offset,
            price: float,
            volume: float,
            stop: bool = False,
            lock: bool = False
    ):
        if self.stop_opening_pos and offset == Offset.OPEN:
            self.write_log("stop_opening_pos=True 所有开仓操作将被屏蔽（仅用于主力合约切换时使用）")
            return []
        else:
            return super().send_order(direction, offset, price, volume, stop, lock)

    def on_order(self, order: OrderData):
        super().on_order(order)
        self.last_order_dt = datetime.now()
        # self.write_log(
        #     f"{order.direction.value} {order.offset.value} {order.price:.1f}"
        #     if order.datetime is None else
        #     f"{datetime_2_str(order.datetime)} {order.direction.value} {order.offset.value} {order.price:.1f}"
        # )
        if not self._is_realtime_mode:
            return
        current_pos = int(self.pos)
        order_datetime = order.datetime
        if order.offset == Offset.OPEN:
            if self.stop_opening_pos:
                addon_str = " 当前策略 stop_opening_pos 开启，所有开仓指令将被忽略"
            else:
                addon_str = ''

            self.write_log(
                f"{order.vt_symbol:>11s} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f} {current_pos:+d} {order.volume:+.0f} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {order.vt_symbol} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f} {current_pos:+d} {order.volume:+.0f}{addon_str}",
                'debug'
            )
        else:
            self.write_log(
                f"{order.vt_symbol:>11s} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f}       {current_pos:+d} {-order.volume:+.0f} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {order.vt_symbol} {order.direction.value} {order.offset.value:4s} "
                f"{order.price:.1f}       {current_pos:+d} {-order.volume:+.0f}",
                'debug'
            )

        if self._last_order is None or self._last_order.orderid != order.orderid:
            self.send_order_list.append(order)
            if self.enable_collect_data:
                order_data_collector.put_nowait(self.strategy_name, order)
            self._last_order = order

    def on_trade(self, trade: TradeData):
        super().on_trade(trade)
        self._trades.append(trade)
        if self.enable_collect_data:
            trade_data_collector.put_nowait(self.strategy_name, trade)

    def on_stop(self):
        super().on_stop()
        if self._is_realtime_mode:
            self._set_strategy_status(AccountStrategyStatusEnum.Stopped)
        self.put_event()
        # if self._is_realtime_mode:
        #     self.report()

    def report(self):
        date_str = date_2_str(self.current_bar.datetime)
        # 处理 trade
        if len(self._trades) > 0:
            trade_df = pd.DataFrame([{
                "datetime": _.datetime.replace(tzinfo=None) if _.datetime is not None else None,
                "symbol": _.symbol,
                "direction": _.direction.value,
                "offset": _.offset.value,
                "price": _.price,
                "volume": _.volume,
                "orderid": _.orderid,
                "tradeid": _.tradeid,
            } for _ in self._trades]).set_index("orderid")
            file_path = get_output_file_path(
                "data", f"trade_{date_str}.csv",
                root_folder_name=self.strategy_name,
            )
            trade_df.to_csv(file_path)
        else:
            trade_df = None
        # 处理 Order
        if len(self.send_order_list) > 0:
            order_df = pd.DataFrame([{
                "datetime": _.datetime.replace(tzinfo=None) if _.datetime is not None else None,
                "symbol": _.symbol,
                "direction": _.direction.value,
                "offset": _.offset.value,
                "price": _.price,
                "volume": _.volume,
                "order_type": _.type.value,
                "orderid": _.orderid,
            } for _ in self.send_order_list]).set_index("orderid")
            file_path = get_output_file_path(
                "data", f"order_{date_str}.csv",
                root_folder_name=self.strategy_name,
            )
            order_df.to_csv(file_path)
            self.logger.info('截止%s下单情况明细：\n%s', datetime_2_str(self.current_bar.datetime), order_df)
        else:
            order_df = None

        # 合并 order trade
        if order_df is not None and trade_df is not None:
            order_trade_df = pd.concat(
                [order_df, trade_df],
                keys=['order', 'trade'],
                axis=1, sort=True,
            )

            file_path = get_output_file_path(
                "data", f"order_trade_{date_str}.csv",
                root_folder_name=self.strategy_name,
            )
            order_trade_df.to_csv(file_path)
            order_trade_df['datetime'] = order_trade_df.apply(
                lambda x: x['order']['datetime'] if pd.isna(x['trade']['datetime']) else x['trade']['datetime'],
                axis=1
            )
            order_trade_df.drop([('order', 'datetime'), ('trade', 'datetime')], axis=1, inplace=True)
            order_trade_df = order_trade_df[[
                ('datetime', ''),
                ('order', 'symbol'),
                ('order', 'direction'),
                ('order', 'offset'),
                ('order', 'price'),
                ('order', 'volume'),
                ('order', 'order_type'),
                ('trade', 'price'),
                ('trade', 'volume'),
                ('trade', 'tradeid'),
            ]]
            order_trade_df.sort_values('datetime', inplace=True)
            file_path = get_output_file_path(
                "data", f"order_trade_{date_str}.xlsx",
                root_folder_name=self.strategy_name,
            )
            order_trade_df.to_excel(file_path)

    def write_log(self, msg: str, logger_method='info'):
        msg = f"{self.strategy_name} {msg}"
        super().write_log(msg)
        getattr(self.logger, logger_method)(msg)


class TargetPosAndPriceTemplate(CtaTemplate):
    # 目标仓位
    target_pos = 0
    # 目标价格
    target_price = 0
    # 建仓基数，建立空头或多头仓位的数量
    base_position = 1

    def set_target_pos(self, target_pos, price=None):
        """设置目标持仓以及价格"""
        self.target_price = self.current_bar.close_price if price is None else price
        self.target_pos = int(target_pos)
        self.handle_pos_2_target()

    def handle_pos_2_target(self):
        """按目标价格及持仓进行处理"""
        self.cancel_all()
        current_pos = self.pos
        price = self.target_price
        volume = abs(self.target_pos - current_pos)
        if 0 <= self.target_pos < current_pos:
            # 减仓
            # self.write_log(f"平多 {current_pos} - > {self.target_pos}")
            self.sell(price, volume)
        elif self.target_pos < 0 < current_pos:
            # 多翻空
            # self.write_log(f"多翻空 {current_pos} - > {self.target_pos}")
            self.sell(price, abs(current_pos))
            self.short(price, abs(self.target_pos))
        elif self.target_pos < current_pos <= 0:
            volume = abs(self.target_pos - current_pos)
            # self.write_log(f"开空 {current_pos} - > {self.target_pos}")
            self.short(price, volume)
        elif current_pos < self.target_pos <= 0:
            # self.write_log(f"平空 {current_pos} - > {self.target_pos}")
            volume = abs(self.target_pos - current_pos)
            self.cover(price, volume)
        elif current_pos < 0 < self.target_pos:
            # self.write_log(f"空翻多 {current_pos} - > {self.target_pos}")
            self.cover(price, abs(current_pos))
            self.buy(price, abs(self.target_pos))
        elif 0 <= current_pos < self.target_pos:
            # self.write_log(f"开多 {current_pos} - > {self.target_pos}")
            volume = abs(self.target_pos - current_pos)
            self.buy(price, volume)


class TargetPosTemplate(TargetPosTemplateBase, CtaTemplate):
    """
        CtaTemplateBase(vnpy原始的 CtaTemplate)
               ↖
        TargetPosTemplateBase               CtaTemplateMixin
                            ↖               ↗
                            TargetPosTemplate
    """

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)


if __name__ == "__main__":
    pass
