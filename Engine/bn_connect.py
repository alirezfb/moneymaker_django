import sys

import requests
from time import sleep
import datetime
import pandas as pd
import random

try:
    from . import tse_time
    from . import my_sql
except:
    import tse_time
    import my_sql

"""
Urls

https://www.binance.com/api/v3/uiKlines?limit=|a number|&symbol=|a symbol|&interval=|a number and interval|
[open time in ms, open, high, low, close, first symbol volume, close time in ms, second symbol volume, ? , ? , ? , ? ]
exp = https://www.binance.com/api/v3/uiKlines?limit=1000&symbol=BTCUSDT&interval=1d
result exp = [1729555200000,"67377.50000000","67800.00000000","66571.42000000","67412.01000000","12812.04614000",1729641599999,"861223810.49169710",1586527,"6207.91768000","417395681.74831470","0"]

"""


class urls:
    def __init__(self, symbol):
        self.symbol = symbol
        pass

    def chart_data(self, interval, limit_num=100):
        return ("https://www.binance.com/api/v3/uiKlines?limit=" +
                str(limit_num) + "&symbol=" + self.symbol +
                "&interval=" + interval)


class binance_connect:
    def __init__(self, symbol):
        self.symbol = symbol
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
        self.urls = urls(symbol)
        self.chart_columns = ['open_time_ms', 'open', 'high', 'low', 'close',
                              'first_sym_vol', 'close_time', 'second_sym_vol',
                              'u0', 'u1', 'u2', 'u3']

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
                    my_sql.log.error_write(self.symbol)
                    return None

    def chart_data(self, interval, limit_num=100):
        return binance_connect.__fetcher(self, self.urls.chart_data(interval, limit_num))

    def dataframe_chart_date(self, url_response):
        return binance_connect.__create_dataframe(self, url_response)

    def __create_dataframe(self, url_response):
        try:
            list_temp: list = url_response.json()
            list_temp.reverse()
            df = pd.DataFrame(list_temp, columns=self.chart_columns)
            binance_connect.__open_time_convert(self, df)
            return df
        except:
            # error handling
            my_sql.log.error_write(self.symbol)
            return None

    def __open_time_convert(self, dataframe):
        try:
            for index_num in range(len(dataframe.index)):
                dataframe.loc[index_num, "open_time"] = datetime.datetime.fromtimestamp(
                    dataframe.loc[index_num, 'open_time_ms'] / 1000.0)
            dataframe.drop('open_time_ms', axis=1, inplace=True)
            return dataframe
        except:
            my_sql.log.error_write(self.symbol)
            return None


a = binance_connect("BTCUSDT")
c = a.chart_data('1h')
b = a.dataframe_chart_date(c)
temp_list = c.json()
print(c.json())
print(b)
my_sql.write_anything(b, "btcusdt", my_sql.binance_object.chart_data())
