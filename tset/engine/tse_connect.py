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
from . import tse_time
from . import my_sql
from time import sleep
import sys
from urllib.request import urlopen, Request
#import pytse_client as tse
import random
from . import tse_analize
import pandas as pd
import numpy as np

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


class HistoryDatabaseUpdate():

    def closing_prices_pd(index, save_limit):
        error_count = 0
        while error_count <= 4:
            try:
                url_template = "https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/"
                url_dates = url_template + index + "/0"

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
                responce_dates_url = requests.get(url_dates, headers=headers[random.randint(0, 2)])
                """df = pd.json_normalize(responce_dates_url.json()['closingPriceDaily'])
                try:
                    df.drop(['priceYesterday', 'priceFirst', 'last', 'id',
                            'iClose', 'yClose', 'pDrCotVal', 'hEven'], axis=1, inplace=True)
                except:
                    pass
                return df"""
                return responce_dates_url
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                    pass
                else:
                    # error handling
                    my_sql.log.error_write(index)
                    return None
                pass
            pass


    def client_types_pd(index, closing_price):
        error_count = 0
        while error_count <= 4:
            try:
                url_template = "https://cdn.tsetmc.com/api/ClientType/GetClientTypeHistory/"
                url_dates = url_template + index

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
                responce_client_types = requests.get(url_dates, headers=headers[random.randint(0,2)])
                """df = pd.json_normalize(responce_client_types.json()['clientType'])
                try:
                    df.drop(['recDate', 'insCode'], axis=1, inplace=True)
                    pass
                except:
                    pass
                closing_price = pd.concat([closing_price, df], axis=1)
                if closing_price is None:
                    return None
                elif len(closing_price.index) < 800:
                    loop_length = len(closing_price.index) - 1
                    pass
                else:
                    loop_length = 800
                    closing_price.drop(closing_price.index[loop_length - 1:closing_price.shape[0]], axis=0, inplace=True)
                    pass
                return closing_price"""
                return responce_client_types
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                    pass
                else:
                    # error handling
                    my_sql.log.error_write(index)
                    return None
                pass
            pass
        # error handling
        my_sql.log.error_write(index)
        return None


    def dataframe_create(client_responce, closing_responce, index):
        try:
            closing_df = HistoryDatabaseUpdate.closing_price_df(index, closing_responce)
            client_df = HistoryDatabaseUpdate.client_types_df(index, closing_df, client_responce)
            del closing_df
            return client_df
        except:
            my_sql.log.error_write(index)

    def closing_price_df(index, url_responce):
        try:
            df = pd.json_normalize(url_responce.json()['closingPriceDaily'])
            try:
                df.drop(['priceYesterday', 'priceFirst', 'last', 'id',
                         'iClose', 'yClose', 'pDrCotVal', 'hEven'], axis=1, inplace=True)
            except:
                pass
            return df
        except:
            # error handling
            my_sql.log.error_write(index)
            return None

    def client_types_df(index, closing_df, url_responce):
        try:
            df = pd.json_normalize(url_responce.json()['clientType'])
            try:
                df.drop(['recDate', 'insCode'], axis=1, inplace=True)
            except:
                pass
            closing_df = pd.concat([closing_df, df], axis=1)
            if closing_df is None:
                return None
            elif len(closing_df.index) < 800:
                loop_length = len(closing_df.index) - 1
                pass
            else:
                loop_length = 800
                closing_df.drop(closing_df.index[loop_length - 1:closing_df.shape[0]], axis=0, inplace=True)
                pass
            return closing_df
        except:
            # error handling
            my_sql.log.error_write(index)
            return None

    @staticmethod
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
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 '
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
                    pass
                else:
                    pass
                pass
            pass
        if error_count >= 10:
            my_sql.log.error_write("0")
            return None
        pass


class LiveDatabaseUpdate():
    def closing_prices_pd(index, save_limit):
        error_count = 0
        while error_count <= 4:
            try:
                url_template = "https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceInfo/"
                url_dates = url_template + index
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
                url_responce = requests.get(url_dates, headers=headers[random.randint(0, 2)])
                return url_responce
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                    pass
                else:
                    # error handling
                    my_sql.log.error_write(index)
                    return None
                pass
            pass
        pass



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
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 '
                                  'Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, '
                                  'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
                }]
                responce_client_types = requests.get(url_dates, headers=headers[random.randint(0, 2)])
                return responce_client_types
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                    pass
                else:
                    # error handling
                    my_sql.log.error_write(index)
                    return None
                pass
            pass
        # error handling
        return None

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
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 '
                                  'Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, '
                                  'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
                }]
                responce_best_limits = requests.get(url_dates, headers=headers[random.randint(0, 2)])
                return responce_best_limits
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                    pass
                else:
                    # error handling
                    my_sql.log.error_write(index)
                    return None
                pass
            pass
        # error handling
        return None

    def dataframe_create(client_responce, closing_responce, index):
        try:
            closing_df = LiveDatabaseUpdate.closing_price_df(index, closing_responce)
            client_df = LiveDatabaseUpdate.client_types_df(index, closing_df, client_responce)
            del closing_df
            return client_df
        except:
            my_sql.log.error_write(index)

    def closing_price_df(index, url_responce):
        try:
            dataframe = pd.json_normalize(url_responce.json()['closingPriceInfo'])
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
            my_sql.log.error_write(index)
            return None

    def client_types_df(index, dataframe, url_responce):
        try:
            temp_dataframe = pd.json_normalize(url_responce.json()['clientType'])
            try:
                temp_dataframe.drop(['buy_DDD_Volume', 'buy_CountDDD'], axis=1, inplace=True)
            except:
                pass
            return_dataframe = pd.concat([dataframe, temp_dataframe], axis=1)
            return return_dataframe
        except:
            # error handling
            my_sql.log.error_write(index)
            return None

    def best_limits_df(index, url_responce):
        try:
            dataframe = pd.json_normalize(url_responce.json()['bestLimits'])
            try:
                dataframe.drop(['insCode'], axis=1, inplace=True)
            except:
                pass
            return dataframe
        except:
            # error handling
            my_sql.log.error_write(index)
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
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 '
                                  'Safari/537.36',
                }, {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, '
                                  'like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
                }]
                responce_dates_url = requests.get(url_dates, headers=headers[random.randint(0, 2)])
                df = pd.json_normalize(responce_dates_url.json()['marketOverview'])
                return df
            except:
                error_count += 1
                if error_count < 4:
                    sleep(random.random())
                    pass
                else:
                    # error handling
                    my_sql.log.error_write("")
                    return None
                pass
            pass


def list_int(list):
    return_list = []
    for i in list:
        return_list.append(int(i))
        pass
    return return_list
