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
        live_object = tse_connect.database_update(index, live=True)
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
        my_sql.log.error_write(index)
        return None


def history_fetcher__(index):
    try:
        tbl_name = "nmd" + str(index)
        # getting saved dates of an index in main database
        # last open day
        market_obj = tse_connect.market_state()
        main_date_list = my_sql.search_dates(tbl_name,
                                             my_sql.obj_properties.tse.moneymaker_history, list_return=True)
        analyze_date_list = my_sql.search_dates(tbl_name,
                                                my_sql.obj_properties.tse.analyze_history, list_return=True)
        last_open = my_sql.read_table("market_status",
                                      my_sql.obj_properties.tse.manager.market_status,
                                      "marketActivityDEven", list_return=False)
        if last_open == main_date_list[0] and last_open == analyze_date_list[0]:
            print('skip')
            return None
        else:
            history_object = tse_connect.database_update(index, live=False)
            # fetching price list from url and saving them
            closing_price_response = history_object.fetch_closing_price()
            # timeout error
            if closing_price_response is None:
                return None
            else:
                # fetching client types parameters and saving them
                client_types_response = history_object.fetch_client_types()
                best_limits_response = history_object.fetch_best_limits()
                pass
            return [client_types_response, closing_price_response, best_limits_response]
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
            history_object = tse_connect.database_update(index, live=False, save_limit=800)
            # getting saved dates of an index in main database
            main_date_list = my_sql.search_dates(tbl_name, moneymaker_obj)
            # getting saved dates of an index in analize database
            analyze_date_list = my_sql.search_dates(tbl_name, analyze_obj)
            # extracting lists form lists
            client_response, closing_response, best_limits_response = response_list
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
                    sum_best_limits = scripts.sum_live_best_limits_generate(live=False)
                    my_sql.write_table(sum_best_limits, tbl_name, sum_best_obj, truncate=True)
                    print(str(index) + " Completed " + str(result))
                    return result
    except:
        my_sql.log.error_write(index)
        return None


def live_write__(response_list, index):
    try:
        tbl_name = "nmd" + index
        moneymaker_obj = my_sql.obj_properties.tse.moneymaker_live
        best_limits_obj = my_sql.obj_properties.tse.best_limits_live
        sum_best_limits_obj = my_sql.obj_properties.tse.sum_live_best_limits
        client_response, closing_response, best_limits_response = response_list
        live_object = tse_connect.database_update(index, live=True)
        if client_response is None or closing_response is None:
            return None
        else:
            pd_dataframe = live_object.dataframe_closing_client(closing_response, client_response)
            best_limits_dataframe = live_object.dataframe_best_limits(best_limits_response)
            script_obj = tse_analize.scripts(index=index, only_status=False, df_return=True)
            if pd_dataframe is None:
                return None
            else:
                # saving price list and client types in database
                my_sql.write_table(pd_dataframe, tbl_name, moneymaker_obj)
                my_sql.write_table(best_limits_dataframe, tbl_name, best_limits_obj)
                sum_best_limit_df = script_obj.sum_live_best_limits_generate()
                my_sql.write_table(sum_best_limit_df, tbl_name, sum_best_limits_obj, truncate=True)
                del pd_dataframe, best_limits_dataframe
        return True
    except:
        my_sql.log.error_write(index)
        return None
