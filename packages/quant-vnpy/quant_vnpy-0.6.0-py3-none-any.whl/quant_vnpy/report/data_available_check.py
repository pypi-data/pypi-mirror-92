"""
@author  : MG
@Time    : 2020/12/25 9:38
@File    : data_available_check.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import logging

from quant_vnpy.constants import INSTRUMENT_TRADE_TIME_PAIR_DIC

from quant_vnpy.db.orm import database
from quant_vnpy.utils.enhancement import get_instrument_type

logger = logging.getLogger()


def data_available_check(symbol='rb2105'):
    """每日早晨检查昨夜夜盘行情是否导入到数据库"""
    sql_str = """SELECT `datetime`, `exchange` FROM dbbardata 
    where symbol=%s and `interval`='1m' order by `datetime` desc limit 1"""
    sql_latest_trade_date_str = """SELECT trade_date FROM trade_date_model
    where trade_date<curdate() order by trade_date desc limit 1
    """
    try:
        trade_date_latest = database.execute_sql(sql_latest_trade_date_str).fetchone()[0]
        row = database.execute_sql(sql_str, [symbol]).fetchone()
        if row is None:
            logger.warning("%-6s 没有数据", symbol)
            return False
        else:
            datetime_max, exchange = row

        instrument_type = get_instrument_type(symbol).upper()
        _, end_time = INSTRUMENT_TRADE_TIME_PAIR_DIC[instrument_type]
        if trade_date_latest <= datetime_max.date() and datetime_max.hour >= end_time.hour - 1:
            logger.info("%6s.%-4s [OK] 预期截止日期 %s 数据截止时间 %s", symbol, exchange, end_time, datetime_max)
            return True
        else:
            logger.info("%6s.%-4s [Not yet] 预期截止日期 %s 数据截止时间 %s", symbol, exchange, end_time, datetime_max)
            return False
    finally:
        database.close()


def _check_symbol_list():
    import itertools
    instrument_type_list = ['rb', 'hc', ]
    contract_year_month_list = ['2105', '2110']
    symbol_list = [instrument_type + year_month for instrument_type, year_month in
                   itertools.product(instrument_type_list, contract_year_month_list)]
    instrument_type_list = ['i', 'j', 'jm', 'm', 'p', 'jd']
    contract_year_month_list = ['2105', '2109']
    symbol_list.extend([instrument_type + year_month for instrument_type, year_month in
                        itertools.product(instrument_type_list, contract_year_month_list)])
    instrument_type_list = ['a', 'y']
    contract_year_month_list = ['2105', '2107']
    symbol_list.extend([instrument_type + year_month for instrument_type, year_month in
                        itertools.product(instrument_type_list, contract_year_month_list)])
    instrument_type_list = ['ap']
    contract_year_month_list = ['105', '110']
    symbol_list.extend([instrument_type + year_month for instrument_type, year_month in
                        itertools.product(instrument_type_list, contract_year_month_list)])
    for symbol in symbol_list:
        data_available_check(symbol)


if __name__ == "__main__":
    _check_symbol_list()
