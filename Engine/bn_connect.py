"""
Urls

https://www.binance.com/api/v3/uiKlines?limit=|a number|&symbol=|a symbol|&interval=|a number and interval|
[open time in ms, open, high, low, close, first symbol volume, close time in ms, second symbol volume, ? , ? , ? , ? , ?]
exp = https://www.binance.com/api/v3/uiKlines?limit=1000&symbol=BTCUSDT&interval=1d
result exp = [1729555200000,"67377.50000000","67800.00000000","66571.42000000","67412.01000000","12812.04614000",1729641599999,"861223810.49169710",1586527,"6207.91768000","417395681.74831470","0"]

"""


class urls:
    def __init__(self, symbol):
        self.symbol = symbol
        pass

    def chart_data(self, interval_num, interval_unit, limit_num=100):
        return ("https://www.binance.com/api/v3/uiKlines?limit=" +
                str(limit_num) + "&symbol=" + self.symbol +
                "&interval=" + str(interval_num) + interval_unit)


a = urls("BTCUSDT")
b = a.chart_data(1, 'd')
print(b)
