# -*- coding: utf-8 -*-
""""
in module baraye test kardane baghie module ha tarahi shode
"""
import sys
# Import Section


from datetime import datetime
import pandas
from time import sleep
import tse_connect
import tse_analize
import my_sql
import tse_time
import extract_save


# Import Section


# START


def live_fetcher__(index):
    try:
        # creating database update class instance
        live_object = tse_connect.DbUpdate(index, live=True)
        # fetching price list from url and saving them
        closing_price_response = live_object.fetch_closing_price()
        # timeout error
        if closing_price_response is None:
            return None
        else:
            # fetching client types parameters and saving them
            best_limits_response = live_object.fetch_best_limits()
            client_types_response = live_object.fetch_client_types()
            pass
        return [client_types_response, closing_price_response, best_limits_response]
    except:
        my_sql.Log.error_write(index)
        return None


def history_fetcher__(index):
    try:
        tbl_name = "nmd" + str(index)
        print(tbl_name)
        # getting saved dates of an index in main database
        # last open day
        market_obj = tse_connect.MarketState()
        last_open = market_obj.last_open()
        obj_dic = {
            "moneymaker": my_sql.ObjProperties.Tse.MoneymakerHistory,
            "analyze": my_sql.ObjProperties.Tse.AnalyzeHistory,
            "market_status": my_sql.ObjProperties.Tse.Manager.MarketStatus
        }
        main_dates = my_sql.search_dates(tbl_name, obj_dic["moneymaker"], list_return=True)
        analyze_dates = my_sql.search_dates(tbl_name, obj_dic["analyze"], list_return=True)
        last_saved = my_sql.read_table("market_status", obj_dic["market_status"],
                                       "marketActivityDEven", list_return=False)
        if last_saved == last_open:
            print('skip')
            return None
        if last_saved == main_dates[0] and last_saved == analyze_dates[0]:
            print('skip')
            return None
        else:
            pass
        history_object = tse_connect.DbUpdate(index, live=False)
        # fetching price list from url and saving them
        closing_price_response = history_object.fetch_closing_price()
        # timeout error
        if closing_price_response is None:
            return None
        else:
            pass
        # fetching client types parameters and saving them
        client_types_response = history_object.fetch_client_types()
        best_limits_response = history_object.fetch_best_limits()
        responses_dic = {
            "closing": closing_price_response,
            "client": client_types_response,
            "best_limits": best_limits_response
        }
        return responses_dic
    except:
        my_sql.Log.error_write(index)
        return None


def history_write__(res_dic: dict, index):
    try:
        if res_dic is None:
            return None
        else:
            pass
        # name
        tbl_name = 'nmd' + str(index)
        obj_dic = {
            "moneymaker": my_sql.ObjProperties.Tse.MoneymakerHistory,
            "analyze": my_sql.ObjProperties.Tse.AnalyzeHistory,
            "market_status": my_sql.ObjProperties.Tse.Manager.MarketStatus,
            "best_limit_obj": my_sql.ObjProperties.Tse.BestLimitsHistory,
            "sum_best_obj": my_sql.ObjProperties.Tse.SumCloseBestLimits
        }
        df_obj = tse_connect.DfCreate(index, live=False, save_limit=800)
        # getting saved dates of an index in main database
        main_dates = my_sql.search_dates(tbl_name, obj_dic["moneymaker"])
        # getting saved dates of an index in analyze database
        analyze_dates = my_sql.search_dates(tbl_name, obj_dic["analyze"])
        # extracting lists form lists
        if res_dic["client"] is None or res_dic["closing"] is None:
            return None
        elif main_dates[0] == tse_time.day_subtract(days_number=1, holiday_check=True):
            return None
        else:
            pass
        # creating dataframe
        main_df = df_obj.joint(res_dic["closing"], res_dic["client"])
        best_limits_df = df_obj.best_limits(res_dic["best_limits"])
        print(best_limits_df)
        if main_df is None:
            return None
        else:
            pass
        my_sql.write_tbl(main_df, tbl_name, obj_dic["moneymaker"], main_dates)
        my_sql.write_tbl(best_limits_df, tbl_name, obj_dic["best_limit_obj"], truncate=True)
        analyze_df: pandas.DataFrame = tse_analize.list_calculate_pd_2(index, pd_dataframe=main_df, live=False)
        del main_df, best_limits_df
        if analyze_df is None:
            return None
        elif analyze_dates[0] == analyze_df.loc[0, 'dEven']:
            return None
        # analyze write
        result = my_sql.write_tbl(analyze_df, tbl_name, obj_dic["analyze"], analyze_dates)
        scripts = tse_analize.scripts(index=index)
        sum_best_limits = scripts.sum_live_best_limits_generate(live=False)
        my_sql.write_tbl(sum_best_limits, tbl_name, obj_dic["sum_best_obj"], truncate=True)
        print(str(index) + " Completed " + str(result))
        return result
    except:
        my_sql.Log.error_write(index)
        return None


def live_write__(response_list, index):
    try:
        tbl_name = "nmd" + index
        # extracting responses
        client_response, closing_response, best_limits_response = response_list
        if client_response is None or closing_response is None:
            return None
        else:
            pass
        # creating object instances
        moneymaker_obj = my_sql.ObjProperties.Tse.MoneymakerLive
        best_limits_obj = my_sql.ObjProperties.Tse.BestLimitsLive
        sum_best_limits_obj = my_sql.ObjProperties.Tse.SumLiveBestLimits
        # creating database class instance
        live_object = tse_connect.DbUpdate(index, live=True)
        pd_dataframe = live_object.dataframe_closing_client(closing_response, client_response)
        if pd_dataframe is None:
            return None
        else:
            pass
        best_limits_dataframe = live_object.dataframe_best_limits(best_limits_response)
        script_obj = tse_analize.scripts(index=index, only_status=False, df_return=True)
        # saving price list and client types in database
        my_sql.write_tbl(pd_dataframe, tbl_name, moneymaker_obj)
        my_sql.write_tbl(best_limits_dataframe, tbl_name, best_limits_obj)
        sum_best_limit_df = script_obj.sum_live_best_limits_generate()
        my_sql.write_tbl(sum_best_limit_df, tbl_name, sum_best_limits_obj, truncate=True)
        return True
    except:
        my_sql.Log.error_write(index)
        return None
