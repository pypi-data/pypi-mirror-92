import sys
from PyFin.api import *
from PyFin.api.Analysis import DELTA
from PyFin.Math.Accumulators import Log
from PyFin.Math.Accumulators import MovingRank
from PyFin.Math.Accumulators.IAccumulators import Pow
from PyFin.Math.Accumulators.StatefulAccumulators import MovingCorrelation
from PyFin.Analysis.CrossSectionValueHolders import CSRankedSecurityValueHolder
from PyFin.Analysis.CrossSectionValueHolders import CSPercentileSecurityValueHolder
from PyFin.Analysis.SecurityValueHolders import SecurityIIFValueHolder
from PyFin.Analysis.SecurityValueHolders import SecurityDeltaValueHolder
from PyFin.Analysis.SecurityValueHolders import SecurityShiftedValueHolder
from PyFin.Analysis.SecurityValueHolders import SecurityLatestValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityMinimumValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityMaximumValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityExpValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecuritySqrtValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecuritySignValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityLogValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecuritySignValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityPowValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatelessTechnicalAnalysers import SecurityXAverageValueHolder
from PyFin.Analysis.TechnicalAnalysis.StatefulTechnicalAnalysers import SecurityMovingMax
from PyFin.Analysis.TechnicalAnalysis import SecurityAbsValueHolder
from PyFin.Analysis.TechnicalAnalysis import SecurityMovingAverage
from PyFin.Analysis.TechnicalAnalysis import SecurityMovingCorrelation
from PyFin.Analysis.TechnicalAnalysis import SecurityMovingSum
from PyFin.Analysis.TechnicalAnalysis import SecurityMovingStandardDeviation
from PyFin.Analysis.TechnicalAnalysis import SecurityMovingRank
from PyFin.Analysis.TechnicalAnalysis import SecurityMovingMin

import datetime as dt
import numpy as np
import numpy.matlib as matlib
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import select, and_

engine = create_engine('postgresql+psycopg2://alpha:alpha@180.166.26.82:8889/alpha')
begin_date = '2018-12-15'
end_date = '2018-12-28'

from sqlalchemy import BigInteger, Column, DateTime, Float, Index, Integer, String, Text, Boolean, text, JSON, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Market(Base):
    __tablename__ = 'market'
    __table_args__ = (
        Index('market_idx', 'trade_date', 'code', unique=True),
    )
    trade_date = Column(DateTime, primary_key=True, nullable=False)
    code = Column(String, primary_key=True, nullable=False)
    secShortName = Column(String(10))
    exchangeCD = Column(String(4))
    preClosePrice = Column(Float(53))
    actPreClosePrice = Column(Float(53))
    openPrice = Column(Float(53))
    highestPrice = Column(Float(53))
    lowestPrice = Column(Float(53))
    closePrice = Column(Float(53))
    turnoverVol = Column(BigInteger)
    turnoverValue = Column(Float(53))
    dealAmount = Column(BigInteger)
    turnoverRate = Column(Float(53))
    accumAdjFactor = Column(Float(53))
    negMarketValue = Column(Float(53))
    marketValue = Column(Float(53))
    chgPct = Column(Float(53))
    PE = Column(Float(53))
    PE1 = Column(Float(53))
    PB = Column(Float(53))
    isOpen = Column(Integer)
    vwap = Column(Float(53))


query = select([Market]).where(
    and_(Market.trade_date >= begin_date, Market.trade_date <= end_date, ))
mkt_df = pd.read_sql(query, engine)
mkt_df.rename(columns={'preClosePrice': 'pre_close', 'openPrice': 'openPrice',
                       'highestPrice': 'highestPrice', 'lowestPrice': 'lowestPrice',
                       'closePrice': 'closePrice', 'turnoverVol': 'turnoverVol',
                       'turnoverValue': 'turnoverValue', 'accumAdjFactor': 'accum_adj',
                       'vwap': 'vwap'}, inplace=True)
mkt_df = mkt_df[[('000000' + str(code))[-6:][0] in '036' for code in mkt_df['code']]]
trade_date_list = list(set(mkt_df.trade_date))
trade_date_list.sort(reverse=True)
mkt_df = mkt_df.set_index('trade_date')
mkt_df = mkt_df[mkt_df['turnoverVol'] > 0]

df = mkt_df.loc['2018-12-28']
df.head(5)

start_pos = '2018-12-15'
end_pos = end_date

# CLOSE>DELAY(CLOSE,1)
expression1 = SecurityLatestValueHolder('closePrice') > SecurityShiftedValueHolder(1,
                                                                                   SecurityLatestValueHolder(
                                                                                       'closePrice'))

# MIN(LOW,DELAY(CLOSE,1))
expression2 = SecurityMinimumValueHolder(SecurityLatestValueHolder('lowestPrice'),
                                         SecurityShiftedValueHolder(1, SecurityLatestValueHolder('closePrice')))

# MAX(HIGH,DELAY(CLOSE,1))
expression3 = SecurityMaximumValueHolder(SecurityLatestValueHolder('lowestPrice'),
                                         SecurityShiftedValueHolder(1, SecurityLatestValueHolder('closePrice')))

# CLOSE-(expression1?expression2:expression3)
expression4 = SecurityLatestValueHolder('closePrice') - SecurityIIFValueHolder(
    expression1, expression2, expression3)

# (CLOSE=DELAY(CLOSE,1)?0:expression4)
# expression5 = SecurityIIFValueHolder(SecurityLatestValueHolder('closePrice') == SecurityShiftedValueHolder(1,
#                                     SecurityLatestValueHolder('closePrice')),
#                                     0, expression4)

expression5 = SecurityIIFValueHolder(SecurityLatestValueHolder('closePrice'),
                                     SecurityLatestValueHolder('closePrice') > SecurityLatestValueHolder('openPrice'),
                                     SecurityLatestValueHolder('openPrice') < SecurityLatestValueHolder('closePrice'))
#
# #-1*SUM(expression5,6)
#
# expression6 = SecurityPowValueHolder(expression5, 1) * (-1.)
# #expression6 = expression5 * (-1.)

name = 'alpha3'
df = mkt_df.loc[start_pos:end_pos].reset_index().set_index('trade_date')
result = expression5.transform(df, name=name, category_field='code', dropna=False)
print(result.sort_values(by='trade_date', ascending=False).head(5))

# N = 2
# expression1 = SecurityXAverageValueHolder(N, SecurityXAverageValueHolder(N, SecurityXAverageValueHolder(N, SecurityLatestValueHolder('closePrice'))))
# expression2 = SecurityXAverageValueHolder(N, SecurityXAverageValueHolder(N, SecurityXAverageValueHolder(N, SecurityLatestValueHolder('pre_close'))))
# TRIX = expression1
#
# name = "TRIX5D"
# df = mkt_df.loc[start_pos:end_pos].reset_index().set_index('trade_date')
# result = TRIX.transform(df, name=name, category_field='code', dropna=False)
# print(result.sort_values(by='trade_date', ascending=False).head(5))
