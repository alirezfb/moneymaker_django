# -*- coding: utf-8 -*-
"""
in module baraye motasel shodan be tse va estekhraje
etelaat az oon tarahi shode
"""
import logging
from typing import List, Any

#from pytse_client import Ticker
import requests
import json
import io
from time import sleep
import sys
from urllib.request import urlopen, Request
#import pytse_client as tse
import random
import pandas as pd
import numpy as np

try:
    from . import tse_time
    from . import my_sql
except:
    import tse_time
    import my_sql

# START


today = tse_time.today_str()

"""
JSON VARIABLES GUIDE

https://cdn.tsetmc.com/api/Codal/GetPreparedDataByInsCode/9/46348559193224090

https://cdn.tsetmc.com/api/ClosingPrice/GetMarketMap?market=0&size=1365&sector=0&typeSelected=1&hEven=0
    daryafte nam va etelaate tamami namadhaye bours
    insCode     #index
    dEven       #tarikh
    hEven       #zaman]
    pClosing        gheymat payani
    pDrCotVal  
    zTotTran
    qTotTran5J
    qTotCap
    priceYesterday
    lVal18AFC
    lSecVal
    percent
    priceChangePercent
    

https://cdn.tsetmc.com/api/BestLimits/(index)/(date)
    etelaate lahzeyi safe kharid va foroosh
    hEven = saat/daghighe/sanie
    number = olaviat gheymat
    qTitMeDem = hajm moamelat kharid
    zOrdMeDem = tedad moamelat kharid
    pMeDem = gheymat moamelat kharid
    pMeOf = gheymat moamelat foroosh
    zOrdMeOf = tedade moamelat foroosh
    qTitMeOf = hajme moamelat foroosh
    

    https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceHistory/(index)/(date)
    etelaate lahzeyi gheymat ha
    hEven = saat/daghighe/sanie
    pClosing = gheymat payani dar hEven
    pDrCotVal = akharin moamele dar hEven
    priceYesterday      #closing diruz
    zTotTran = tedad moamelat
    qTotTran5J = hajme moamelat
    qTotCap = arzesh moamelat
    priceChange     #pDrCotVal - priceYesterday
    
    
https://cdn.tsetmc.com/api/Shareholder/(index)/(date)
    etelaate sahamdaran
    shareHolderID = id sahamdar
    shareHolderName = name sahamdar
    cIsin = shenase sahamdar
    dEven = tarikhe rooz
    numberOfShares = meghdar saham
    perOfShares = darsad saham
    changeAmount = meghdare taghir
    
    
https://cdn.tsetmc.com/api/Trade/GetTradeHistory/46348559193224090/20240909/true
    etelaate history gheymat
    nTran       tedad moamelat
    hEven       saat/daghighe/sanie
    qTitTran        ?
    pTran       akahrin moamele
    


                        https://cdn.tsetmc.com/api/Trade/GetTrade/46348559193224090
    etelaate lahzeyi gheymat ha
    "insCode":  -
    "dEven":    -
    "nTran":        tedad moamelat
    "hEven":        akharin saat/daghighe/sanie baz boodan
    "qTitTran":         ?
    "pTran":        akharin moamele
    "qTitNgJ": -
    "iSensVarP": -
    "pPhSeaCotJ": -
    "pPbSeaCotJ": -
    "iAnuTran": -
    "xqVarPJDrPRf": -
    "canceled": -
    

https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/(index)/0
    etelaate roozane gheymathaye namad
    priceMin        #payintarin gheymat
    priceMax        #balatarin gheymat
    priceYesterday      #closing diruz
    priceFirst      #opening 
    insCode     #shenase namad
    dEven       #tarikhe rooz
    hEven       #akharin zamane baz boodan bazar
    pClosing        #gheymat payani
    pDrCotVal       #akharin moamele
    qTotTran5J      #hajme moamelat
    qTotCap     #arzesh moamelat
    priceChange     #pDrCotVal - priceYesterday
    
    
https://cdn.tsetmc.com/api/ClosingPrice/GetRelatedCompany/27
    hamgorooh haye yek namad
    lVal30      #esme kamel namad
    insCode     #code namad
    priceChange     #pDrCotVal - priceYesterday
    priceMin        #payintarin gheymat
    priceMax        #balatarin gheymat
    priceYesterday      #closing diruz
    pClosing        #gheymat payani
    pDrCotVal       #akharin moamele
    qTotTran5J      #hajme moamelat
    zTotTran        #akharin gheymat
    qTotTran5J      #hajme moamelat
    qTotCap     #arzesh moamelat
    
    

https://cdn.tsetmc.com/api/BestLimits/46348559193224090
    akharin etelate safe moamelat baste shode rooz
    number      #olaviat kharid
    qTitMeDem       #hajm kharid 
    zOrdMeDem       #tedad kharid
    pMeDem      #gheymat kharid
    pMeOf       #gheymat foroosh
    zOrdMeOf        #olaviat foroosh
    qTitMeOf        #hajm foroosh
    
    
    
https://cdn.tsetmc.com/api/ClientType/GetClientTypeHistory/(index)/(date)
    
    
https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDaily/(index)/(date)

https://cdn.tsetmc.com/api/MarketData/GetStaticThreshold/(index)/(date)

https://cdn.tsetmc.com/api/MarketData/GetInstrumentState/(index)/(date)


    qTotTran5J = hajm koli moamelat
    qTotCap = arzesh koli moamelat
    zTotTran = tedad moamelat
    priceMax = bishtarin gheymat
    priceMin = kamtarin gheymat
    priceYesterday = gheymat closing diruz
    priceFirst = gheymat avalie bazgoshayi
    priceChange = taghirat gheymat payani
    
    

https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/46348559193224090/12


https://cdn.tsetmc.com/api/ClientType/GetClientType/46348559193224090/1/0
    akharin etelaate lahzeyi namad
    *
    buy_I_Volume        hajme kharid haghighi
    buy_N_Volume        hajme kharid hoghoghi
    buy_DDD_Volume      ?
    buy_CountI      tedad kharid haghihgih
    buy_CountN      tedad kharid hoghoghi
    buy_CountDDD        ?
    sell_I_Volume       hajme forosh haghighi
    sell_N_Volume       hajme foroosh hoghooghi
    sell_N_Volume       hajme foroosh hoghooghi
    sell_CountI     tedad foroosh haghighi
    sell_CountN     tedad foroosh hoghooghi
    


https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/46348559193224090
    *
    in url etelaate ghemyat tablo lahzeyi dar akharin rooze baze namad ro mide
    lastHEven       #akharin saate baze namad
    finalLastDate      #akharin tarikhe baz boodane namad
    priceMin        #bishine ghaymat
    priceMax       #bishtarin gheymat
    priceYesterday      #closing diruz
    priceFirst      #opening emrooz
    pClosing        #gheymat  payani
    pDrCotVal       #akharin moamele
    zTotTran        #tedad
    qTotTran5J      #hajm
    qTotCap     #arzesh
    
    
https://cdn.tsetmc.com/api/MarketData/GetMarketOverview/0
    in safhe vaziat va shakhes haye bours hastesh
    indexLastValue      #shakhes kol
    indexChange     #taghirat shakhes
    indexEqualWeightedLastValue     #shakhes kol ham vazn
    indexEqualWeightedChange        #taghirat shakhes kol hamvazn
    marketActivityDEven     #akharin tarikhe baz boodan bazar
    marketActivityHEven     #akharin zamane baz boodan bazar
    marketActivityZTotTran      #tedad moamelat
    marketActivityQTotCap       #arzesh moamelat
    marketActivityQTotTran      #hajm moamelat
    marketState     #baste boodan bazar ehtemalat F va T
    marketValue     #arzesh bazar
    marketStateTitle        #baste boodan bazar ya baz boodan
    
    
https://cdn.tsetmc.com/api/Index/GetIndexB1LastAll/SelectedIndexes/1
    shakhes haye bours
    insCode     #code shakhes
    xDrNivJIdx004       #shakhesh kol
    xPhNivJIdx004       #bishtarin shakhes
    xPbNivJIdx004       #kamtarin shakhes
    xVarIdxJRfV     #taghirat shakhes
    indexChange     #taghirat shakhes
    lVal30      #symbol shakhes
    
    
    
https://cdn.tsetmc.com/api/Index/GetIndexB1LastAll/SelectedIndexes/2
    shakhes haye fara bours
    insCode     #code shakhes
    xDrNivJIdx004       #shakhesh kol
    xPhNivJIdx004       #bishtarin shakhes
    xPbNivJIdx004       #kamtarin shakhes
    xVarIdxJRfV     #taghirat shakhes
    indexChange     #taghirat shakhes
    lVal30      #symbol shakhes
    

https://cdn.tsetmc.com/api/ClosingPrice/GetTradeTop/MostVisited/1/7
    namad haye por tarakonesh bours
    priceChange     #tafrighe priceyesterday va pDrCotVal
    priceMin        #bishine
    priceMax        #bishtarin  
    priceYesterday      #closing diruz
    priceFirst      #opening
    insCode     #code namad
    dEven       #tarikh baz boodan
    pClosing        #closing emrooz
    pDrCotVal       #akhrin moamele
    zTotTran        #tedad
    qTotTran5J      #hajm
    qTotCap     #arzesh
    
    
https://cdn.tsetmc.com/api/ClosingPrice/GetTradeTop/MostVisited/2/7
    namad haye por tarakonesh fara bours
    lVal18AFC       #symbol namad
    priceChange     #tafrighe priceyesterday va pDrCotVal
    priceMin        #bishine
    priceMax        #bishtarin  
    priceYesterday      #closing diruz
    priceFirst      #opening
    insCode     #code namad
    dEven       #tarikh baz boodan
    pClosing        #closing emrooz
    pDrCotVal       #akhrin moamele
    zTotTran        #tedad
    qTotTran5J      #hajm
    qTotCap     #arzesh
    
    
https://cdn.tsetmc.com/api/Index/GetInstEffect/0/1/7
    namad haye bours ha ba bishtarin tasir bar shakhes
    lVal18AFC       #symbol namad
    pClosing        gheymat closing
    instEffectValue         #tasir
    


https://cdn.tsetmc.com/api/Index/GetInstEffect/0/2/7
    namad haye farabours ha ba bishtarin tasir bar shakhes
    lVal18AFC       #symbol namad
    pClosing        gheymat closing
    instEffectValue         #tasir
    
https://cdn.tsetmc.com/api/StaticData/GetTime
    gereftane tarikh va zaman
    


"""

"""
in tabe baraye estekhraje namad va return karde oon hatesh
"""


class urls:
    def __init__(self):
        pass

    headers = [{
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/109.0.0.0 Safari/537.36',
    }, {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 '
                      'Safari/537.36',
    }, {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, '
                      'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
    }]

    class tse_history:
        def __init__(self, index):
            self.index = str(index)

        def url_closing_price(self):
            return "https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/" + self.index + "/0"

        def url_client_types(self):
            return "https://cdn.tsetmc.com/api/ClientType/GetClientTypeHistory/" + self.index

        def url_best_limit(self):
            return "https://cdn.tsetmc.com/api/BestLimits/" + self.index

        drop_columns_closing_price = ['priceYesterday', 'priceFirst', 'last', 'id',
                                      'iClose', 'yClose', 'pDrCotVal', 'hEven', 'insCode']
        drop_columns_best_limits = ['insCode']
        drop_columns_client_types = ['recDate', 'insCode']
        json_name_closing_price = 'closingPriceDaily'
        json_name_client_types = 'clientType'
        json_name_best_limits = 'bestLimits'

    class tse_live:
        def __init__(self, index):
            self.index = str(index)

        def url_closing_price(self):
            return "https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/" + self.index

        def url_client_types(self):
            return "https://cdn.tsetmc.com/api/ClientType/GetClientType/" + self.index + "/1/0"

        def url_best_limit(self):
            return "https://cdn.tsetmc.com/api/BestLimits/" + self.index

        drop_columns_closing_price = ['instrument', 'nvt', 'mop', 'pRedTran', 'dEven', 'hEven',
                                      'thirtyDayClosingHistory', 'priceChange', 'last', 'id',
                                      'iClose', 'yClose', 'insCode', 'instrumentState.idn',
                                      'instrumentState.dEven', 'instrumentState.hEven',
                                      'instrumentState.insCode', 'instrumentState.lVal18AFC',
                                      'instrumentState.lVal30', 'instrumentState.cEtaval',
                                      'instrumentState.realHeven', 'instrumentState.underSupervision',
                                      'instrumentState.cEtavalTitle']
        drop_columns_best_limits = ['insCode']
        drop_columns_client_types = ['buy_DDD_Volume', 'buy_CountDDD']


class DbUpdate:
    def __init__(self, index: str, live: bool, save_limit: int = 0):
        self.index = index
        self.headers = urls.headers
        self.save_limit = save_limit
        if live is True:
            self.object = urls.tse_live(index)
        else:
            self.object = urls.tse_history(index)

    def __fetcher(self, url_address):
        error_count = 0
        while error_count <= 4:
            try:
                return requests.get(url_address, headers=self.headers[random.randint(0, 2)])
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                else:
                    # error handling
                    my_sql.Log.error_write(self.index)
                    return None

    def fetch_closing_price(self):
        return DbUpdate.__fetcher(self, self.object.url_closing_price())

    def fetch_client_types(self):
        return DbUpdate.__fetcher(self, self.object.url_client_types())

    def fetch_best_limits(self):
        return DbUpdate.__fetcher(self, self.object.url_best_limit())

    def dataframe_closing_client(self, closing_response, client_response):
        try:
            closing_df = DbUpdate.__create_dataframe(self, closing_response, self.object.json_name_closing_price,
                                                     self.object.drop_columns_closing_price)
            client_df = DbUpdate.__create_dataframe(self, client_response, self.object.json_name_client_types,
                                                    self.object.drop_columns_client_types)
            # return none if empty
            if closing_df is None or client_df is None:
                return None
            # comparing length of dataframes
            else:
                pass
            return_df = pd.DataFrame()
            if len(closing_df.index) > len(client_df.index):
                return_df = pd.concat([closing_df, client_df], axis=1)
                loop_length = len(closing_df.index) - 1
            else:
                return_df = pd.concat([client_df, closing_df], axis=1)
                loop_length = len(client_df.index) - 1
            return_df.drop(return_df.index[loop_length - 1:return_df.shape[0]], axis=0, inplace=True)
            return return_df
        except:
            my_sql.Log.error_write(self.index)
            return None

    def dataframe_best_limits(self, url_response):
        return DbUpdate.__create_dataframe(self, url_response,
                                           self.object.json_name_best_limits,
                                           self.object.drop_columns_best_limits)

    def __create_dataframe(self, url_response, json_name, drop_columns):
        try:
            df = pd.json_normalize(url_response.json()[json_name])
            try:
                df.drop(drop_columns, axis=1, inplace=True)
            except:
                pass
            if self.save_limit > 0:
                if len(df.index) < self.save_limit:
                    loop_length = len(df.index) - 1
                else:
                    loop_length = self.save_limit
                    df.drop(df.index[loop_length - 1:df.shape[0]], axis=0, inplace=True)
            return df
        except:
            # error handling
            my_sql.Log.error_write(self.index)
            return None


class DfCreate:
    def __init__(self, index: str, live: bool, save_limit: int = 0):
        self.index = index
        self.save_limit = save_limit
        if live is True:
            self.object = urls.tse_live(index)
        else:
            self.object = urls.tse_history(index)

    def joint(self, closing_response, client_response):
        try:
            closing_df = DfCreate.__create_df(self, closing_response, self.object.json_name_closing_price,
                                              self.object.drop_columns_closing_price)
            client_df = DfCreate.__create_df(self, client_response, self.object.json_name_client_types,
                                             self.object.drop_columns_client_types)
            # return none if empty
            if closing_df is None or client_df is None:
                return None
            # comparing length of dataframes
            else:
                pass
            return_df = pd.DataFrame()
            if len(closing_df.index) > len(client_df.index):
                return_df = pd.concat([closing_df, client_df], axis=1)
                loop_length = len(closing_df.index) - 1
            else:
                return_df = pd.concat([client_df, closing_df], axis=1)
                loop_length = len(client_df.index) - 1
            return_df.drop(return_df.index[loop_length - 1:return_df.shape[0]], axis=0, inplace=True)
            return return_df
        except:
            my_sql.Log.error_write(self.index)
            return None

    def best_limits(self, url_response):
        return DfCreate.__create_df(self, url_response,
                                    self.object.json_name_best_limits,
                                    self.object.drop_columns_best_limits)

    def __create_df(self, url_response, json_name, drop_columns):
        try:
            df = pd.json_normalize(url_response.json()[json_name])
            try:
                df.drop(drop_columns, axis=1, inplace=True)
            except:
                pass
            if self.save_limit > 0:
                if len(df.index) < self.save_limit:
                    loop_length = len(df.index) - 1
                else:
                    loop_length = self.save_limit
                    df.drop(df.index[loop_length - 1:df.shape[0]], axis=0, inplace=True)
            return df
        except:
            # error handling
            my_sql.Log.error_write(self.index)
            return None



def tblnamadha_update():
    error_count = 0
    error_message = ""
    while error_count < 10:
        try:
            url_template = "https://cdn.tsetmc.com/api/ClosingPrice/GetMarketMap?market=0&size=1365&sector=0&typeSelected=1&hEven=0"

            headers = [{
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/109.0.0.0 Safari/537.36',
            }, {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/77.0.3865.90'
                              'Safari/537.36',
            }, {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, '
                              'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
            }]
            responce_dates_url = requests.get(url_template, headers=headers[random.randint(0, 2)])
            df = pd.json_normalize(responce_dates_url.json())
            return df
        except:
            error_count += 1
            if error_count > 4:
                sleep(random.random())
            else:
                pass
    if error_count >= 10:
        my_sql.Log.error_write("0")
        return None


class LiveDatabaseUpdate:
    def __init__(self):
        pass

    @staticmethod
    def closing_prices_pd(index, save_limit):
        error_count = 0
        while error_count <= 4:
            try:
                url_template = 'https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/'
                url_dates = url_template + index
                headers = [{
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/109.0.0.0 Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/77.0.3865.90'
                                  'Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 ('
                                  'KHTML,'
                                  'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
                }]
                url_response = requests.get(url_dates, headers=headers[random.randint(0, 2)])
                return url_response
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                else:
                    # error handling
                    my_sql.Log.error_write(index)
                    return None

    @staticmethod
    def client_types_pd(index, closing_price):
        error_count = 0
        while error_count <= 4:
            try:
                url_template = "https://cdn.tsetmc.com/api/ClientType/GetClientType/"
                url_dates = url_template + index + "/1/0"
                headers = [{
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/109.0.0.0 Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/77.0.3865.90'
                                  'Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 ('
                                  'KHTML,'
                                  'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
                }]
                response_client_types = requests.get(url_dates, headers=headers[random.randint(0, 2)])
                return response_client_types
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                else:
                    # error handling
                    my_sql.Log.error_write(index)
                    return None
        return None

    @staticmethod
    def best_limits_pd(index):
        error_count = 0
        while error_count <= 4:
            try:
                url_template = "https://cdn.tsetmc.com/api/BestLimits/"
                url_dates = url_template + index
                headers = [{
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/109.0.0.0 Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/77.0.3865.90'
                                  'Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 ('
                                  'KHTML,'
                                  'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
                }]
                response_best_limits = requests.get(url_dates, headers=headers[random.randint(0, 2)])
                return response_best_limits
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                else:
                    # error handling
                    my_sql.Log.error_write(index)
                    return None
        # error handling
        return None

    @staticmethod
    def dataframe_create(client_response, closing_response, index):
        try:
            closing_df = LiveDatabaseUpdate.closing_price_df(index, closing_response)
            client_df = LiveDatabaseUpdate.client_types_df(index, closing_df, client_response)
            del closing_df
            return client_df
        except:
            my_sql.Log.error_write(index)

    @staticmethod
    def closing_price_df(index, url_response):
        try:
            dataframe = pd.json_normalize(url_response.json()['closingPriceInfo'])
            try:
                dataframe.drop(['instrument', 'nvt', 'mop', 'pRedTran', 'dEven', 'hEven',
                                'thirtyDayClosingHistory', 'priceChange', 'last', 'id',
                                'iClose', 'yClose', 'insCode', 'instrumentState.idn',
                                'instrumentState.dEven', 'instrumentState.hEven',
                                'instrumentState.insCode', 'instrumentState.lVal18AFC',
                                'instrumentState.lVal30', 'instrumentState.cEtaval',
                                'instrumentState.realHeven', 'instrumentState.underSupervision',
                                'instrumentState.cEtavalTitle'], axis=1, inplace=True)
            except:
                pass
            return dataframe
        except:
            # error handling
            my_sql.Log.error_write(index)
            return None

    @staticmethod
    def client_types_df(index, dataframe, url_response):
        try:
            temp_dataframe = pd.json_normalize(url_response.json()['clientType'])
            try:
                temp_dataframe.drop(['buy_DDD_Volume', 'buy_CountDDD'], axis=1, inplace=True)
            except:
                pass
            return_dataframe = pd.concat([dataframe, temp_dataframe], axis=1)
            return return_dataframe
        except:
            # error handling
            my_sql.Log.error_write(index)
            return None

    @staticmethod
    def best_limits_df(index, url_response):
        try:
            dataframe = pd.json_normalize(url_response.json()['bestLimits'])
            try:
                dataframe.drop(['insCode'], axis=1, inplace=True)
            except:
                pass
            return dataframe
        except:
            # error handling
            my_sql.Log.error_write(index)
            return None

    @staticmethod
    def market_overview():
        error_count = 0
        while error_count <= 4:
            try:
                url_dates = "https://cdn.tsetmc.com/api/MarketData/GetMarketOverview/1"
                headers = [{
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/109.0.0.0 Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/77.0.3865.90'
                                  'Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 ('
                                  'KHTML,'
                                  'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
                }]
                response_dates_url = requests.get(url_dates, headers=headers[random.randint(0, 2)])
                df = pd.json_normalize(response_dates_url.json()['marketOverview'])
                return df
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                else:
                    # error handling
                    my_sql.Log.error_write("")
                    return None


def list_int(list):
    return_list = []
    for i in list:
        return_list.append(int(i))
        pass
    return return_list


class MarketState:
    def __init__(self):
        self.url = "https://cdn.tsetmc.com/api/MarketData/GetMarketOverview/0"
        self.headers = [{
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/109.0.0.0 Safari/537.36',
        }, {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 '
                          'Safari/537.36',
        }, {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, '
                          'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        }]
        self.response = MarketState.__response(self)
        self.dataframe = MarketState.__create_dataframe(self)

    def __response(self):
        for i in range(0, 2):
            try:
                req = requests.get(self.url, headers=self.headers[random.randint(0, 2)])
                return req
            except:
                if i > 1:
                    my_sql.Log.error_write("")
                    return None
                else:
                    sleep(random.randint(0, 2))

    def __create_dataframe(self):
        try:
            return pd.json_normalize(self.response.json()["marketOverview"])
        except:
            my_sql.Log.error_write("")
            return None

    def state(self):
        try:
            if self.dataframe.loc[0, "marketState"] == "T":
                return True
            else:
                return False
        except:
            my_sql.Log.error_write("")
            return None

    def last_open(self):
        try:
            return self.dataframe.loc[0, "marketActivityDEven"]
        except:
            my_sql.Log.error_write("")
            return None
