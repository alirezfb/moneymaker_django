# -*- coding: utf-8 -*-
""""
in module baraye test kardane baghie module ha tarahi shode
"""


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
        # fetching price list from url and saving them
        closing_price_responce = extract_save.UrlFetcher.closing_price_download_pd(index, live=True)
        # timeout error
        if closing_price_responce is None:
            return None
        else:
            # fetching client types parameters and saving them
            client_types = extract_save.UrlFetcher.client_types_download_pd(index, closing_price_responce, live=True)
            best_limits = extract_save.UrlFetcher.best_limits_fetch(index)
            pass
        return [client_types, closing_price_responce, best_limits]
    except:
        my_sql.log.error_write(index)
        return None


def history_fetcher__(index):
    try:
        # getting saved dates of an index in main database
        last_saved_day = my_sql.search.dates(index)[0]
        # last open day
        market_obj = tse_connect.market_state()
        last_open = my_sql.read_table("market_status",
                                      my_sql.obj_properties.tse.manager.market_status,
                                      "marketActivityDEven", list_return=False)
        print(str(last_saved_day) + " " + str(last_open))
        if last_open == last_saved_day:
            print(1)
            return None
        else:
            print(2)
            history_object = tse_connect.history_database(index)
            # fetching price list from url and saving them
            closing_price_response = history_object.fetch_closing_price()
            best_limits_response = history_object.fetch_best_limits()
            # timeout error
            if closing_price_response is None:
                return None
            else:
                # fetching client types parameters and saving them
                client_types = history_object.fetch_client_types()
                pass
            return [client_types, closing_price_response, best_limits_response]
    except:
        my_sql.log.error_write(index)
        return None


def history_write__(response_list, index):
    try:
        if response_list is None:
            return None
        else:
            # name
            tbl_name = 'nmd' + str(index)
            moneymaker_obj = my_sql.obj_properties.tse.moneymaker_history
            best_limit_obj = my_sql.obj_properties.tse.best_limits_history
            analyze_obj = my_sql.obj_properties.tse.analyze_history
            sum_best_obj = my_sql.obj_properties.tse.sum_close_best_limits
            history_object = tse_connect.history_database(index, save_limit=800)
            # getting saved dates of an index in main database
            main_date_list = my_sql.search.dates(index)
            # getting saved dates of an index in analize database
            analyze_date_list = my_sql.search.dates(index, schema="analize")
            # extracting lists form lists
            client_response = response_list[0]
            closing_response = response_list[1]
            best_limits_response = response_list[2]
            if client_response is None or closing_response is None:
                return None
            elif main_date_list[0] == tse_time.day_subtract(days_number=1, holiday_check=True):
                return None
            else:
                # creating dataframe
                pd_dataframe = history_object.dataframe_closing_client(closing_response, client_response)
                best_limits_dataframe = history_object.dataframe_best_limits(best_limits_response)
                del client_response, closing_response, best_limits_response
                if pd_dataframe is None:
                    return None
                else:
                    my_sql.write_table(pd_dataframe, tbl_name, moneymaker_obj, main_date_list)
                    my_sql.write_table(best_limits_dataframe, tbl_name, best_limit_obj, truncate=True)
                    analyze_df: pandas.DataFrame = tse_analize.list_calculate_pd_2(index, pd_dataframe=pd_dataframe, live=False)
                    del pd_dataframe, best_limits_dataframe
                    if analyze_df is None:
                        return None
                    elif analyze_date_list[0] == analyze_df.loc[0, 'dEven']:
                        return None
                    # analyze write
                    result = my_sql.write_table(analyze_df, tbl_name, analyze_obj, analyze_date_list)
                    scripts = tse_analize.scripts(index=index)
                    sum_best_limits = scripts.sum_close_best_limits(live=False)
                    my_sql.write_table(sum_best_limits, tbl_name, sum_best_obj, truncate=True)
                    print(str(index) + " Completed " + str(result))
                    return result
    except:
        my_sql.log.error_write(index)
        return None


def live_write__(responce_list, index):
    try:
        moneymaker_obj = my_sql.obj_properties.tse.moneymaker_live
        best_limits_obj = my_sql.obj_properties.tse.best_limits_live
        tbl_name = "nmd" + index
        client_responce = responce_list[0]
        closing_responce = responce_list[1]
        best_limits = responce_list[2]
        if client_responce is None or closing_responce is None:
            return None
        else:
            pd_dataframe = tse_connect.LiveDatabaseUpdate.dataframe_create(client_responce, closing_responce, index)
            best_linmits_df = tse_connect.LiveDatabaseUpdate.best_limits_df(index, best_limits)
            if pd_dataframe is None:
                return None
            else:
                # saving price list and client types in database
                my_sql.write_table(pd_dataframe, tbl_name, moneymaker_obj)
                my_sql.write_table(best_linmits_df, tbl_name, best_limits_obj)
                del pd_dataframe, best_linmits_df
        return True
    except:
        my_sql.log.error_write(index)
        return None
