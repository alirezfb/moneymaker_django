# -*- coding: utf-8 -*-
""""
in module baraye check karda, extract va save kardane
parameter va rooz haye jadid hastesh
"""
import sys
import threading
import pandas as pd

# Import Section

import pandas
from concurrent.futures import ProcessPoolExecutor
from time import sleep
try:
    from . import my_sql
    from . import tse_time
    from . import tse_connect
    from . import tse_analize
except:
    import my_sql
    import tse_time
    import tse_connect
    import tse_analize
# Import Section


# START

def common_member(a, b):
    try:
        a_set = set(a)
        b_set = set(b)

        # check length
        if len(a_set.intersection(b_set)) > 0:
            return list(a_set.intersection(b_set))
        else:
            return []
    except:
        my_sql.log.error_write("")
        return []


def multiprocess_function_list(func, loop_list, *args):
    try:
        result_list = []
        with ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(func, i, *args) for i in loop_list]
        for future in futures:
            result_list.append(future.result())
        return result_list
    except:
        my_sql.log.error_write("")
        return None


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


def market_status():
    market_state = tse_connect.market_state()
    data = {'todayDEven': [tse_time.today_int()],
            'marketActivityDEven': [int(market_state.last_open())]}

    # Create DataFrame
    df = pd.DataFrame(data)
    my_sql.write_table(df, "market_status",
                       my_sql.obj_properties.tse.manager.market_status)

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


def best_limit_bulk(dataframe, obj, live: bool = True):
    if live is True:
        tbl_name = "bulk_live_best"
    else:
        tbl_name = "bulk_close_best"
    # saving into database
    my_sql.write_table(dataframe, tbl_name, obj, truncate=True)


def compare_lists(index_list: list, definition, df_return: bool = False, rename_sum: bool = True, tbl_save=False, save_obj=None):
    try:
        if df_return is False:
            return_object = index_list.copy()
            status_list = multiprocess_function_list(tse_analize.record_status_return,
                                                     index_list, definition)
            for i in range(0, len(index_list)-1):
                if status_list[i] is True:
                    continue
                else:
                    return_object.remove(index_list[i])
        else:
            dataframe_list = multiprocess_function_list(tse_analize.dataframe_return,
                                                        index_list, definition, rename_sum)
            temp_list = dataframe_list.copy()
            for i in range(0, len(index_list)):
                if dataframe_list[i] is not None:
                    if tbl_save is True:
                        tbl_name = 'nmd' + str(index_list[i])
                        my_sql.write_table(dataframe_list[i], tbl_name, save_obj, truncate=True)
                    else:
                        pass
                    continue
                else:
                    temp_list.remove(index_list[i])
            return_object = temp_list[0]
            del temp_list[0]
            for df in temp_list:
                return_object = pd.concat([return_object, df], axis=0, ignore_index=True)
        return return_object
    except:
        my_sql.log.error_write("")
        return None


def multi_list_compare(index_list, *args, df_return: bool = False, rename_sum: bool = True, tbl_save=False, save_obj=None):
    try:
        multi_list = []
        for definition in args:
            multi_list.append(compare_lists(index_list, definition, df_return=df_return, rename_sum=rename_sum, tbl_save=tbl_save, save_obj=save_obj))
        return_list = multi_list[0]
        for i in range(1, len(multi_list)):
            return_list = common_member(return_list, multi_list[i])
        return return_list
    except:
        my_sql.log.error_write("")


def JointDataframe(index, mode: str):
    #counter = 0
    analize_df = my_sql.read.all_tables(index, 'analize')
    moneymaker_df = my_sql.read.all_tables(index, 'moneymaker')
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
            pd_dataframe: pandas.DataFrame = my_sql.read.all_tables(index, schema='moneymaker')
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

