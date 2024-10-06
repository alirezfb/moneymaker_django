# -*- coding: utf-8 -*-
""""
in module baraye check karda, extract va save kardane
parameter va rooz haye jadid hastesh
"""
import sys
import threading
from . import tse_time
import pandas as pd

# Import Section
from . import tse_connect
from . import tse_analize
import pandas
from . import my_sql
from . import tse_time
from time import sleep


# Import Section


# START

class UrlFetcher:

    def closing_price_download_pd(index, live: bool=True):
        try:
            if live is True:
                closing_price_list = tse_connect.LiveDatabaseUpdate.closing_prices_pd(index=index, save_limit=180)
                pass
            else:
                closing_price_list = tse_connect.HistoryDatabaseUpdate.closing_prices_pd(index=index, save_limit=180)
                pass
            return closing_price_list
        except:
            my_sql.log.error_write(index)
            return None

    def client_types_download_pd(index, closing_price_df: pandas.DataFrame, live: bool):
        try:
            if live is True:
                client_types_list = tse_connect.LiveDatabaseUpdate.client_types_pd(index=index,
                                                                                   closing_price=closing_price_df)
                pass
            else:
                client_types_list = tse_connect.HistoryDatabaseUpdate.client_types_pd(index=index,
                                                                                   closing_price=closing_price_df)
                pass
            return client_types_list
        except:
            my_sql.log.error_write(index)
            return None
        pass

    def best_limits_fetch(index):
        try:
            best_limits_response = tse_connect.LiveDatabaseUpdate.best_limits_pd(index=index)
            return best_limits_response
        except:
            my_sql.log.error_write(index)
            return None
        pass

    def market_overview(only_state=False):
        try:
            market_overview = tse_connect.LiveDatabaseUpdate.market_overview()
            if only_state is False:
                return market_overview
            else:
                state = market_overview.loc[0, 'marketState']
                del market_overview
                if state == 'F':
                    return False
                else:
                    return True
                pass

            pass
        except:
            my_sql.log.error_write("")
            return None
        pass

    pass

"""class filter:

    def closed_best_limits(only_state=False):
        index_list = my_sql.read.index()
        selected_indexes: list = []
        for index in index_list:
            result_df: pandas.DataFrame = tse_analize.scripts.close_best_limit()
            if result_df is None or len(result_df.index) < 1:
                continue
            else:
                selected_indexes.append(index)
            del result_df
        return selected_indexes
    def best_limits_ghodrat_kh(only_state=False):
        index_list = my_sql.read.index()
        selected_indexes: list = []
        for index in index_list:
            result_df: pandas.DataFrame = tse_analize.filter.latest_minute_best_limit(index)
            if result_df is None or len(result_df.index) < 1:
                continue
            else:
                result_df_ = tse_analize.filter.latest_ghodrat_kh_ha(index)
                if result_df_ is None or len(result_df_.index) < 1:
                    continue
                else:
                    selected_indexes.append(index)
                    pass
                pass
            del result_df_, result_df
        return selected_indexes
    @staticmethod
    def top_hajme_haghighi():
        index_list = my_sql.read.index()
        results: list = []
        for index in index_list:
            result = tse_analize.filter.close_best_limit(index)
            if result is not None:
                results.append(result)
                pass
            else:
                pass
            pass
        pass"""
def database_writing_loop_pd(index, pd_df: pandas.DataFrame):
    try:
        numbers_list = []
        namad_symbol = my_sql.search.names(self=index)
        tse_dataframe_length = len(pd_df.index)
        # tarif moteghayerhaye controli loop
        six_month = int(tse_time.six_month())
        duplicate_date_count = 0
        row_save_count = 0

        """ Payane tarif motheghayerha"""
        # loop zakhire sazi namad_object
        if pd_df is None:
            return None
        else:
            pass
        for day_count in range(0, 180):
            # check kardane inke az tool namad_object rad nashode bashe
            if day_count >= (tse_dataframe_length - 1):
                break
                pass
            # check kardane inke az 6 mah rad nashe
            elif pd_df.loc[0, 'dEven'] <= six_month:
                break
                pass
            else:
                numbers_list.append(day_count)
                row_save_count += 1
                pass
        print("Running queries for " + namad_symbol + " for " +
              str(len(numbers_list) - 1) + " days.")
        result = my_sql.write.daily_operation_pd_2(dataframe=pd_df)
        return result
    except:
        my_sql.log.error_write(index)


def price_list(index, pd_df: pandas.DataFrame, tbl_dates=None):
    try:
        numbers_list = []
        namad_symbol = my_sql.search.names(self=index)
        tse_dataframe_length = len(pd_df.index)
        """six_month = my_sql.tse_time.six_month()
        # tarif moteghayerhaye controli loop
        duplicate_date_count = 0
        row_save_count = 0
        # loop zakhire sazi namad_object
        if pd_df is None:
            return None
        else:
            pass
        for day_count in range(0, tse_dataframe_length):
            # check kardane inke az tool namad_object rad nashode bashe
            if day_count >= (tse_dataframe_length - 1):
                break
                pass
            # check kardane inke az 6 mah rad nashe
            elif pd_df.loc[0, 'dEven'] <= six_month:
                break
                pass
            else:
                numbers_list.append(day_count)
                row_save_count += 1
                pass"""
        print("Running queries for " + namad_symbol + " for " +
              str(len(numbers_list) - 1) + " days.")
        result = my_sql.Write.HistoryMoneymaker(dataframe=pd_df)
        return result
    except:
        my_sql.log.error_write(index)
        return None


def JointDataframe(index, mode: str):
    #counter = 0
    analize_df = my_sql.read.MoneyMakerTables(index, 'analize')
    moneymaker_df = my_sql.read.MoneyMakerTables(index, 'moneymaker')
    if mode == 'negative':
        analize_df, moneymaker_df = tse_analize.filter.before_negative(index, analize_df.copy(deep=False),
                                                                       moneymaker_df.copy(deep=False))
        pass
    elif mode == 'positive':
        analize_df, moneymaker_df = tse_analize.filter.before_positive(index, analize_df.copy(deep=False),
                                                                       moneymaker_df.copy(deep=False))
        pass
    elif mode == 'none':
        pass
    else:
        # when mode is none of the above
        # raise warning error
        return None
    moneymaker_df.drop(['dEven'], axis=1, inplace=True)
    final_df = pandas.concat([analize_df, moneymaker_df], axis=1)
    return final_df


"""def csv_save(index, df, path):
    temp_dic:dict = tse_analize.filter.counter(index, df)
    #dic_negative_temp:dict = tse_analize.filter.counter(i, dic_negative_df)
    for j in dic_negative.keys():
        dic_negative[j].append(dic_negative_temp[j])
        dic_positive[j].append(dic_positive_temp[j])
        pass
    counter += 1"""

"""csv_positive = pd.DataFrame.from_dict(dic_positive)
    csv_negative = pd.DataFrame.from_dict(dic_negative)
    path = r'E:\Programming\projects\python\Moneymaker\Moneymaker\csv'
    csv_positive.to_csv(path+'csv1.csv')"""


def analize_list(index, pd_df: pandas.DataFrame, tbl_dates: list = None):
    try:
        numbers_list = []
        namad_symbol = my_sql.search.names(self=index)
        """tse_dataframe_length = len(pd_df.index)
        # tarif moteghayerhaye controli loop
        six_month = int(tse_time.six_month())
        row_save_count = 0
    
        # loop zakhire sazi namad_object
        if pd_df is None:
            return None
        else:
            pass
        for day_count in range(0, 180):
            # check kardane inke az tool namad_object rad nashode bashe
            if day_count >= (tse_dataframe_length - 1):
                break
                pass
            # check kardane inke az 6 mah rad nashe
            elif pd_df.loc[0, 'dEven'] <= six_month:
                break
                pass
            else:
                numbers_list.append(day_count)
                row_save_count += 1
                pass
            pass"""
        print("Running queries for " + namad_symbol + " for " +
              str(len(numbers_list) - 1) + " days.")
        result = my_sql.Write.analize_list_daily(dataframe=pd_df)
        return result
    except:
        return None

def black_list_check(index_list):
    for index in index_list:
        try:
            pd_dataframe: pandas.DataFrame = my_sql.read.MoneyMakerTables(index, schema='moneymaker')
            """closing_price_df = UrlFetcher.closing_price_download_pd(index, live=False)
            client_types_df = UrlFetcher.client_types_download_pd(index, closing_price_df=closing_price_df, live=False)"""
            client_types_df = None
            closing_price_df = None
            if pd_dataframe is None or len(pd_dataframe.index) == 0:
                if client_types_df is None or closing_price_df is None:
                    temp_list:list = [[index]]
                    bl_dataframe: pandas.DataFrame = pd.DataFrame(temp_list, columns=['insCode'])
                    my_sql.black_list.write(bl_dataframe)
                    pass
                else:
                    pass
            else:
                pass
        except:
            my_sql.log.error_write(index)
            continue
            pass
        pass
    return True



class BackgroundServices(threading.Thread):
    @staticmethod
    def price_save(index, dataframe, tbl_dates=None):
        try:
            result = price_list(index, dataframe, tbl_dates)
            return result
        except:
            my_sql.log.error_write(index)
            return None
        pass

    @staticmethod
    def analyze_save(index, dataframe, tbl_dates=None):
        try:
            result = analize_list(index, dataframe, tbl_dates)
            return result
        except:
            my_sql.log.error_write(index)
            return None
        pass
