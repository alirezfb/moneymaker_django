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


def multiprocess_function(func, *args):
    with ProcessPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(square, i) for i in range(5)]
        res = exc1.map(func, *args)
        exc1.shutdown()
    return list(res)


def live_update(index_list, state_check=True):
    start_time_t = datetime.now()
    market_state = extract_save.UrlFetcher.market_overview(only_state=True)
    if state_check is True and market_state is False:
        return 'Market Closed'
    else:
        with ThreadPoolExecutor(max_workers=70) as exc0:
            responce_list = exc0.map(tse_test.live_fetcher__, index_list)
            exc0.shutdown()
            pass
        with ProcessPoolExecutor(max_workers=20) as exc1:
            exc1.map(tse_test.live_write__, responce_list, index_list)
            exc1.shutdown()
            pass
        end_time_t = datetime.now()
        print(" time= " + str(((end_time_t - start_time_t).seconds / 60)))
        return None


def history_update(index_list):
    start_time_t = datetime.now()
    with ThreadPoolExecutor(max_workers=80) as exc0:
        responce_list = exc0.map(tse_test.history_fetcher__, index_list)
        exc0.shutdown()
        pass
    with ProcessPoolExecutor(max_workers=14) as exc1:
        exc1.map(tse_test.history_write__, responce_list, index_list)
        exc1.shutdown()
        pass
    end_time_t = datetime.now()
    print(" time= " + str(((end_time_t - start_time_t).seconds / 60)))
    return None


def infinity_run():
    if __name__ == '__main__':
        endless = True
        index_list = my_sql.read.index(bl_check=True)
        # updateing last open day and today
        extract_save.market_status()
        while endless is True:
            # my_sql.LiveTableCreate.price_table()
            market_state = extract_save.UrlFetcher.market_overview(only_state=True)
            while market_state is True:
                live_update(index_list, state_check=True)
                live_best_limits = tse_analize.dataframe_return(index_list, "sum_live_best_limit")
                temp_index = tse_analize.list_compare_old(index_list, "read_sum_live_best_limit",
                                                      "latest_ha_be_ho")
                live_best_limits = tse_analize.dataframe_return(temp_index, "sum_live_best_limit")
                sleep(190)
                pass
            if market_state is False:
                print("MARKET CLOSED")
                history_update(index_list)
                temp_index = tse_analize.list_compare_old(index_list, "close_best_limit", "close_ghodrat_kh_ha")
                print(temp_index)
                #temp_index = multiprocess_function(tse_analize.list_compare, index_list, "close_best_limit", "close_ghodrat_kh_ha")
                close_best_limits = tse_analize.dataframe_return(temp_index, "all_close_best_limit", rename=False)
                print(close_best_limits)
                extract_save.best_limit_bulk(close_best_limits,
                                             my_sql.obj_properties.tse.best_limits_live, live=False)
                print('done')
                sleep(300)
                pass
            else:
                print("WTF")
                pass
            sleep(3600)

if __name__ == '__main__':
    infinity_run()
