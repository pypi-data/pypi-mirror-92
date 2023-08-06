# -*- coding:utf-8 -*-
import trdb2py.trading2_pb2
from datetime import datetime


def analysisResult(result: dict, dtFormat: str = '%Y-%m-%d') -> dict:
    if len(result['pnl'].values) > 0:
        startdt = datetime.fromtimestamp(
            result['pnl'].values[0].ts).strftime(dtFormat)

        enddt = datetime.fromtimestamp(
            result['pnl'].values[len(result['pnl'].values)-1].ts).strftime(dtFormat)

        valuesnums = len(result['pnl'].values)

        if len(result['pnl'].lstCtrl) > 0:
            buynums = 0
            sellnums = 0
            winnums = 0

            for v in result['pnl'].lstCtrl:
                if v.type == trdb2py.trading2_pb2.CtrlType.CTRL_SELL:
                    sellnums = sellnums + 1
                    if v.sellPrice > v.averageHoldingPrice:
                        winnums = winnums + 1
                if v.type == trdb2py.trading2_pb2.CtrlType.CTRL_BUY:
                    buynums = buynums + 1

            winrate = 0
            if sellnums > 0:
                winrate = winnums / sellnums

            return {'startTime': startdt, 'endTime': enddt, 'valuesNums': valuesnums,
                    'buyNums': buynums, 'sellNums': sellnums, 'winNums': winnums, 'winRate': winrate}

        return {'startTime': startdt, 'endTime': enddt, 'valuesNums': valuesnums}

    return None
