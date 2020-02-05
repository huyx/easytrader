from typing import Dict, List

import pandas as pd

from easytrader import grid_strategies
from easytrader.clienttrader import ClientTrader
from easytrader.config.client import CommonConfig


class HAITONG(CommonConfig):
    BALANCE_CONTROL_ID_GROUP = {
        "资金余额": 1012,
        "冻结资金": 1013,
        "可用金额": 1016,
        "可取金额": 1017,
        # 海通客户端中，“股票市值”控件不可见，运行时会出错。暂时的解决方法不获取股票市值
        # "股票市值": 1014,
        "总资产": 1015,
    }

    GRID_DTYPE = {
        "操作日期": str,
        "委托编号": str,
        "申请编号": str,
        "合同编号": str,
        "证券代码": str,
        "股东代码": str,
        "资金帐号": str,
        "资金帐户": str,
        "发生日期": str,
    }


class HaitongXls(grid_strategies.Xls):
    def _format_grid_data(self, filename: str) -> List[Dict]:
        """分析保存的 csv 文件

        海通客户端导出的 csv 文件比较特殊。标题中采用的是 ',' 作为分隔符，而下面的数据采用的是 '\t' 作为分隔符。
        """
        df = pd.read_csv(
            filename,
            encoding='gbk',
            engine='python',
            delimiter="[,\t]",
            dtype=self._trader.config.GRID_DTYPE,
            na_filter=False,
        )
        return df.to_dict("records")


class HaitongClientTrader(ClientTrader):
    """海通客户端

    - 获取表格数据时，如果用拷贝模式，则需要输入验证码。因此默认采用保存 xls 文件模式。
    """
    grid_strategy = HaitongXls

    # noinspection PyMissingConstructor
    def __init__(self):
        self._config = HAITONG
        self._app = None
        self._main = None

    @property
    def broker_type(self):
        return 'haitong'
