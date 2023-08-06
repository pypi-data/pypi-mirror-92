# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os; os.chdir("S:/siat")
from siat.transaction import *


df=security_price('600519.SS','2020-1-1','2020-12-31',power=5)

compare_security(["AAPL","MSFT"],"Annual Ret Volatility%","2020-1-1","2020-12-31")



df=security_price('600519.SS','2020-1-1','2020-12-31',power=5)

compare_security(["AAPL","MSFT"],"Daily Ret%","2020-1-1","2020-12-31")

compare_security("MSFT",["Daily Ret%","Annual Ret%"],"2020-1-1","2020-12-31")

compare_security("AAPL",["Daily Ret%","Annual Ret%"],"2020-1-1","2020-12-31")

compare_security(["AAPL","MSFT"],"Annual Ret%","2020-1-1","2020-12-31")

compare_security(["AAPL","MSFT"],"Annual Adj Ret%","2020-1-1","2020-12-31")

compare_security(["TWTR","FB"],"Annual Ret%","2020-1-1","2020-12-31")

compare_security(["600519.SS","000858.SZ"],"Annual Adj Ret%","2020-1-1","2020-12-31")

compare_security(["DAI.DE","BMW.DE"],"Annual Adj Ret%","2020-1-1","2020-12-31")

compare_security(["7203.T","7201.T"],"Annual Adj Ret%","2020-1-1","2020-12-31")

compare_security(["4911.T","4452.T"],"Annual Adj Ret%","2020-1-1","2020-12-31")

compare_security(["9983.T","7453.T"],"Annual Adj Ret%","2020-1-1","2020-12-31")







compare_security(["000001.SS","399001.SZ"],"Close","2020-1-1","2020-12-31", twinx=True)

df=security_price('000001.SS','2020-1-1','2020-12-31',power=5)

compare_security(["000001.SS","^HSI"],"Close","2020-1-1","2020-12-31", twinx=True)

compare_security(["000001.SS","^N225"],"Close","2020-1-1","2020-12-31", twinx=True)

compare_security(["000001.SS","^KS11"],"Close","2020-1-1","2020-12-31", twinx=True)

compare_security(["^KS11","^N225"],"Close","2020-1-1","2020-12-31", twinx=True)

compare_security(["000001.SS","^DJI"],"Close","2020-1-1","2020-12-31", twinx=True)

compare_security(["^DJI","^GSPC"],"Close","2020-1-1","2020-12-31", twinx=True)



df=security_price('6BH22.CME','2020-10-1','2021-1-31',power=4)

compare_security(["ZT=F","ZF=F"],"Exp Ret%","2010-1-1","2020-6-30")
compare_security(["ZN=F","ZB=F"],"Exp Ret%","2010-1-1","2020-6-30")

compare_security(["ZT=F","ZF=F"],"Exp Ret Volatility%","2010-1-1","2020-6-30")
compare_security(["ZN=F","ZB=F"],"Exp Ret Volatility%","2010-1-1","2020-6-30")


compare_security(["ES=F","^GSPC"],"Close","2020-1-1","2020-12-31")

compare_security(["ES=F","^GSPC"],"Close","2020-10-1","2020-12-31")

compare_security(["ES=F","^GSPC"],"Close","2020-12-1","2020-12-31")

compare_security(["ES=F","^GSPC"],"Close","2020-11-1","2020-12-31")


compare_security(["ES=F","^GSPC"],"Close","2020-12-1","2021-1-15")
compare_security(["ES=F","^GSPC"],"Annual Price Volatility","2020-12-1","2021-1-15")
compare_security(["ES=F","^GSPC"],"Exp Ret%","2020-12-1","2021-1-15")
compare_security(["ES=F","^GSPC"],"Exp Ret Volatility","2020-12-1","2021-1-15")



df=security_price('MSFT','2021-1-1','2021-1-31',datatag=True,power=4)

info=get_stock_profile("AAPL")
info=get_stock_profile("MSFT",info_type='officers')
info=get_stock_profile("AAPL",info_type='officers')
info=stock_info('AAPL')
sub_info=stock_officers(info)

div=stock_dividend('600519.SS','2011-1-1','2020-12-31')
split=stock_split('600519.SS','2000-1-1','2020-12-31')

ticker='AAPL'
info=stock_info(ticker)
info=get_stock_profile("AAPL",info_type='officers')

info=get_stock_profile("AAPL")

info=get_stock_profile("MSFT",info_type='officers')
info=get_stock_profile("GS",info_type='officers')

info=stock_info('JD')
sub_info=stock_officers(info)
info=get_stock_profile("JD",info_type='officers')

info=stock_info('BABA')
sub_info=stock_officers(info)
info=get_stock_profile("BABA",info_type='officers')

info=stock_info('0700.HK')
sub_info=stock_officers(info)
info=get_stock_profile("0700.HK",info_type='officers')

info=stock_info('600519.SS')
sub_info=stock_officers(info)
info=get_stock_profile("600519.SS",info_type='officers')

info=get_stock_profile("0939.HK",info_type='risk_esg')


market={'Market':('China','^HSI')}
stocks={'0700.HK':3,'9618.HK':2,'9988.HK':1}
portfolio=dict(market,**stocks)
esg=portfolio_esg2(portfolio)



