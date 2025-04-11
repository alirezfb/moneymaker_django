from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from datetime import datetime
from time import sleep
try:
    from . import tse_analize
    from . import tse_test
    from . import extract_save
    from . import my_sql
except:
    import tse_analize
    import tse_test
    import extract_save
    import my_sql

# 46348559193224090

"""def multiprocess_return(index_list, definition):
    with ProcessPoolExecutor(max_workers=20) as exc1:
        locals()[func_name]("Alice")
        exc1.map(definition, responce_list, index_list)
        exc1.shutdown()
        pass
    return None"""


def multiprocess_function_list(func, loop_list, *args):
    result_list = []
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(func, i, *args) for i in loop_list]
    for future in futures:
        result_list.append(future.result())
    return result_list


def live_update(index_list, state_check=True):
    # start timing
    start_time_t = datetime.now()
    # if market state hasn't been checked
    if state_check is True:
        # checking again if market is open
        market_state = extract_save.UrlFetcher.market_overview(only_state=True)
        if market_state is False:
            return 'Market Closed'
        else:
            pass
    else:
        with ThreadPoolExecutor(max_workers=8) as exc0:
            response_list = exc0.map(tse_test.live_fetcher__, index_list)
            exc0.shutdown()
            pass
        with ProcessPoolExecutor(max_workers=4) as exc1:
            exc1.map(tse_test.live_write__, response_list, index_list)
            exc1.shutdown()
            pass
        end_time_t = datetime.now()
        print(" time= " + str(((end_time_t - start_time_t).seconds / 60)))
        return None


def history_update(index_list):
    start_time_t = datetime.now()
    with ThreadPoolExecutor(max_workers=8) as exc0:
        response_list = exc0.map(tse_test.history_fetcher__, index_list)
        exc0.shutdown()
        pass
    with ProcessPoolExecutor(max_workers=4) as exc1:
        exc1.map(tse_test.history_write__, response_list, index_list)
        exc1.shutdown()
        pass
    end_time_t = datetime.now()
    print(" time= " + str(((end_time_t - start_time_t).seconds / 60)))
    return None


def infinity_run():
    if __name__ == '__main__':
        # whether it should run endlessly or from 9 to 12:30
        endless = True
        # reading index list
        index_list = my_sql.Read.index(bl_check=True)
        index_list = ['46348559193224090']
        #index_list = index_list[:30]
        # updating last open day and latest day this program had run
        extract_save.market_status()
        while endless is True:
            # my_sql.LiveTableCreate.price_table()
            # checking if market is open
            market_state = extract_save.UrlFetcher.market_overview(only_state=True)
            #if market is open
            while market_state is True:
                # initiate live update for main and analyze table
                live_update(index_list, state_check=True)
                print('fff')
                # live_best_limits = tse_analize.dataframe_return_old(index_list, "sum_live_best_limit")
                live_best_limits = extract_save.multi_list_compare(index_list, "sum_live_best_limit", df_return=True)
                print(live_best_limits)
                extract_save.bulk_dataframe_save(live_best_limits, index_list,
                                                 my_sql.ObjProperties.Tse.SumLiveBestLimits)
                print('koom')
                """temp_index = tse_analize.list_compare_old(index_list, "read_sum_live_best_limit",
                                                      "latest_ha_be_ho")"""
                temp_index = extract_save.multi_list_compare(index_list, "read_sum_live_best_limit",
                                                             "latest_ha_be_ho")
                print(temp_index)
                extract_save.best_limit_bulk(temp_index,
                                             my_sql.ObjProperties.Tse.BulkSomeCloseBestLimits, live=True)
                print('motherfucker')
                pass
            if market_state is False:
                print("MARKET CLOSED")
                history_update(index_list)
                print('f1')
                sleep(100)
                close_best_limits = extract_save.multi_list_compare(index_list, "sum_close_best_limits_generate",
                                                                    df_return=True, tbl_save=True, rename_sum=False,
                                                                    save_obj=my_sql.ObjProperties.Tse.SumCloseBestLimits)

                print('f2')
                sleep(10)
                # temp_index = tse_analize.list_compare_old(index_list, "close_best_limit", "close_ghodrat_kh_ha")
                temp_index = extract_save.multi_list_compare(index_list, "sum_close_best_limit_read", "close_ghodrat_kh_ha")
                print(temp_index)
                # temp_index = multiprocess_function(tse_analize.list_compare, index_list, "close_best_limit", "close_ghodrat_kh_ha")
                # close_best_limits = tse_analize.dataframe_return_old(temp_index, "all_close_best_limit", rename=False)
                close_best_limits = extract_save.multi_list_compare(temp_index, "sum_close_best_limit_read",
                                                                    df_return=True, rename_sum=True)
                print(close_best_limits)
                extract_save.best_limit_bulk(close_best_limits,
                                             my_sql.ObjProperties.Tse.BulkSomeCloseBestLimits, live=False)
                print('done')
                pass
            else:
                print("WTF")
                pass
            sleep(3600)


if __name__ == '__main__':
    infinity_run()
