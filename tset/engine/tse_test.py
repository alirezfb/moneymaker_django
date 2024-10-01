# -*- coding: utf-8 -*-
""""
in module baraye test kardane baghie module ha tarahi shode
"""
import sys

import pandas

# Import Section

import tse_connect as tse_connect
import tse_analize
import my_sql
from datetime import datetime
import tse_time
import extract_save
from concurrent.futures import ProcessPoolExecutor
import threading
import multiprocessing
from time import sleep

"""import sys
from time import sleep
import concurrent.futures
import numpy as np
import pandas as pd
from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool
import mariadb
import multiprocessing"""

# Import Section


# START_
"""
namad = tse_connect.namad("فولاد")
natije = tse_connect.parameter(namad, "None")
natije = tse_analize.listCalculate(natije)
"""

"""result = my_sql.namadTableCreator()
print(result)"""

# khanadan va save kardane esme nanmadha az sql dar liste list_namadha
"""list_namadha_temp = my_sql.read.names()
list_namadha = []
count = 0
for i in list_namadha_temp:
    count += 1
    list_namadha.append(i)
    if count == 30: 
        break
        pass
    else:
        pass
    pass"""


def database_optimize():
    dataframe = tse_connect.HistoryDatabaseUpdate.tblnamadha_update()
    my_sql.Write.tblnamadha_update(dataframe)
    my_sql.HistoryTableCreate.price_table()
    my_sql.HistoryTableCreate.analize_table()
    return True


class BackgroundPriceSave(threading.Thread):
    def run(self, index, client_types, tbl_dates):
        result = extract_save.price_list(index, client_types, tbl_dates)
        return result

    pass


class BackgroundAnalizeSave(threading.Thread):
    def run(self, index, pd_dataframe, analyze_date_list):
        result = extract_save.analize_list(index, pd_dataframe, analyze_date_list)
        return result


class FetchingBackgroundTasks(threading.Thread):
    def run(self, *args, **kwargs):
        index = args[0]
        # fetching price list from url and saving them
        closing_price_df = extract_save.UrlFetcher.closing_price_download_pd(index)
        # fetching client types parameters and saving them
        client_types = extract_save.UrlFetcher.client_types_download_pd(index, closing_price_df)
        pd_dataframe: pandas.DataFrame = tse_analize.list_calculate_pd_2(index, pd_dataframe=client_types)
        return closing_price_df, client_types, pd_dataframe


def Old_HistoryUpdate__(index):
    # this is for application runtime timing
    start_time_t = datetime.now()
    # name of the symbol
    namad_symbol = my_sql.search.names(index)
    # table name in sql
    table_name = 'nmd' + str(index)
    # black list check variable
    bl_temp = False
    # blacklist check
    if bl_temp:
        print("Skipping " + namad_symbol + " because of blacklist.")
        return 0
    else:
        # background I/O tasks
        # backgroud_fetching = FetchingBackgroundTasks(daemon=True)
        # closing_price_df, client_types, pd_dataframe = backgroud_fetching.run(index)
        # getting saved dates of an index in main database
        main_date_list = my_sql.search.dates(index)
        # getting saved dates of an index in analize database
        analyze_date_list = my_sql.search.dates(index, schema="analize")
        # checking if today has already been saved in db
        if main_date_list[0] == tse_time.day_subtract(days_number=1, holiday_check=True):
            print("Skipping " + namad_symbol + " because of last day check.")
            return 0
        else:
            # fetching price list from url and saving them
            closing_price_df = extract_save.UrlFetcher.closing_price_download_pd(index, live=False)
            # timeout error
            if closing_price_df is None:
                print("Skip" + namad_symbol + " because of closing price timeout.")
                return 0
            # duplicate date check
            elif main_date_list[0] == closing_price_df.loc[0, 'dEven']:
                print("Skipping " + namad_symbol + " because of last day check 2.")
                return 0
            else:
                # fetching client types parameters and saving them
                client_types = extract_save.UrlFetcher.client_types_download_pd(index, closing_price_df, live=False)
                del closing_price_df
                # timout error
                if client_types is None:
                    print("Skip" + namad_symbol + " because of client types timeout.")
                    return 0
                else:
                    # saving price list and client types in database
                    my_sql.Write.HistoryMoneymaker(client_types, index)
                    """background_price_save = extract_save.BackgroundServices(daemon=True)
                    background_price_save.price_save(index, client_types.copy(deep=False))"""
                    # creating analyze list dataframe
                    pd_dataframe: pandas.DataFrame = tse_analize.list_calculate_pd_2(index, pd_dataframe=client_types,
                                                                                     live=False)
                    del client_types
                    if pd_dataframe is None:
                        print("Skip" + namad_symbol + " because of analyze list timeout.")
                        return 0
                    elif analyze_date_list[0] == pd_dataframe.loc[0, 'dEven']:
                        print("skipping because of analyze list last day check")
                        return 0
                    else:
                        # saving analyze list into database
                        result = my_sql.Write.analize_list_daily(pd_dataframe, index=index, tbl_dates=analyze_date_list)
                        del analyze_date_list
                        """background_analyze_save = extract_save.BackgroundServices(daemon=True)
                        background_analyze_save.analyze_save(index=index, dataframe=pd_dataframe)"""
                        # print(str(result) + ' days have been saved for ' + my_sql.search.names(index))
                        end_time_t = datetime.now()
                        print(namad_symbol + " time= " + str(((end_time_t - start_time_t).seconds / 60)))
                        return result
                        pass
                    pass
                pass
            pass
        pass
    return 0
    pass

def OldLiveUpdate__(index):
    # black list check variable
    bl_temp = False
    # blacklist check
    if bl_temp:
        return 0
    else:
        # fetching price list from url and saving them
        closing_price_df = extract_save.UrlFetcher.closing_price_download_pd(index, live=True)
        # timeout error
        if closing_price_df is None:
            return 0
        else:
            # fetching client types parameters and saving them
            client_types = extract_save.UrlFetcher.client_types_download_pd(index, closing_price_df, live=True)
            del closing_price_df
            # timout error
            if client_types is None:
                return 0
            else:
                # saving price list and client types in database
                my_sql.Write.LiveSchema(dataframe=client_types, analyze=False, index=index)
                # creating analyze list dataframe
                del client_types
                pd_dataframe = None
                if pd_dataframe is None:
                    return 0
                else:
                    # saving analyze list into database
                    result = my_sql.Write.LiveSchema(dataframe=pd_dataframe, analyze=True, index=index)
                    return result
                    pass
                pass
            pass
        pass
    return 0
    pass


def live_fetcher__(index):
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
def history_fetcher__(index):
    # fetching price list from url and saving them
    closing_price_responce = extract_save.UrlFetcher.closing_price_download_pd(index, live=False)
    # timeout error
    if closing_price_responce is None:
        return None
    else:
        # fetching client types parameters and saving them
        client_types = extract_save.UrlFetcher.client_types_download_pd(index, closing_price_responce, live=False)
        pass
    print('do')
    return [client_types, closing_price_responce]


def history_write__(responce_list, index):
    # getting saved dates of an index in main database
    main_date_list = my_sql.search.dates(index)
    # getting saved dates of an index in analize database
    analyze_date_list = my_sql.search.dates(index, schema="analize")
    client_responce = responce_list[0]
    closing_responce = responce_list[1]
    if client_responce is None or closing_responce is None:
        return None
    elif main_date_list[0] == tse_time.day_subtract(days_number=1, holiday_check=True):
        return None
    else:
        pd_dataframe = tse_connect.HistoryDatabaseUpdate.dataframe_create(client_responce, closing_responce, index)
        print(55)
        del client_responce, closing_responce
        if pd_dataframe is None:
            return None
        else:
            my_sql.Write.HistoryMoneymaker(pd_dataframe, index)
            print(99)
            analyze_df: pandas.DataFrame = tse_analize.list_calculate_pd_2(index, pd_dataframe=pd_dataframe, live=False)
            del pd_dataframe
            if analyze_df is None:
                return None
            elif analyze_date_list[0] == analyze_df.loc[0, 'dEven']:
                return None
            result = my_sql.Write.analize_list_daily(analyze_df, index=index, tbl_dates=analyze_date_list)
            print(str(index) + " Completed " + str(result))
            return result


def live_write__(responce_list, index):
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
            my_sql.Write.LiveSchema(dataframe=pd_dataframe, analyze=False, index=index)
            my_sql.Write.live_best_limits(index, best_linmits_df)
            del pd_dataframe, best_linmits_df
    return True


#my_sql.test("46348559193224090")
"""HistoryUpdate("46348559193224090")
sleep(3300)"""
"""LiveUpdate("46348559193224090")
sleep(3300)"""

"""for i in index_list:
    redemption_thread_pd(i)
    pass"""


def infinity():
    condition = True
    while condition is True:
        OldLiveUpdate__("46348559193224090")
        sleep(15)
        pass


def daily_operation(index):
    parameter = extract_save.parameter_download(index)
    dataframe = extract_save.dataframe_create(parameter)
    result = extract_save.database_writing_loop(dataframe)
    if result is None:
        return 0
    else:
        return result
    pass


def multithread(index_list):
    loop_length = len(index_list) - 1
    start_point = 0
    end_point = 0
    while end_point < loop_length:
        st_time = datetime.now()
        print("end " + str(end_point))
        print("len " + str(loop_length))
        threads = []
        b = []
        end_point += 50
        if end_point > loop_length:
            end_point = loop_length
            pass
        else:
            pass

        """pool = concurrent.futures.ThreadPoolExecutor(max_workers=120)
        for counter in range(start_point, end_point):
            pool.submit(redemption_thread_pd, index_list[counter])
        pool.shutdown(wait=True)"""
        for counter in range(start_point, end_point):
            t = threading.Thread(target=Old_HistoryUpdate__, args=(index_list[counter],))
            threads.append(t)
            t.start()
            pass
        for t in threads:
            t.join()
            pass
        start_point += 50
        en_time = datetime.now()
        print("operation time= " + str(((en_time - st_time).seconds / 60)))
        pass
    pass


def MultithreadSingle(index_list):
    loop_length = len(index_list) - 1
    start_point = 0
    end_point = 0
    while end_point < loop_length:
        st_time = datetime.now()
        print("end " + str(end_point))
        print("len " + str(loop_length))
        threads = []
        b = []
        end_point += 50
        if end_point > loop_length:
            end_point = loop_length
            pass
        else:
            pass

        """pool = concurrent.futures.ThreadPoolExecutor(max_workers=120)
        for counter in range(start_point, end_point):
            pool.submit(redemption_thread_pd, index_list[counter])
        pool.shutdown(wait=True)"""
        for counter in range(start_point, end_point):
            t = threading.Thread(target=Old_HistoryUpdate__, args=(index_list[counter],))
            threads.append(t)
            t.start()
            pass
        for t in threads:
            t.join()
            pass
        start_point += 50
        en_time = datetime.now()
        print("operation time= " + str(((en_time - st_time).seconds / 60)))
        pass
    pass


"""def MultiProcessing():
    if __name__ == '__main__':
        with ProcessPoolExecutor(max_workers=3) as executor:
            results = executor.map(pfff,[0,1,2])
    for r in results:
        print(r)"""

"""thread_count = int((len(index_list) - 1) / 3)
print("Runing the whole operation with " + str(thread_count) + " threads in:")
for i in reversed(range(0, 10)):
    print(i)
    sleep(1)
    pass"""
"""thread_pool = pool.ThreadPool(processes=8)
dataframes = thread_pool.map(redemption, index_list)"""

"""thread_pool = pool.ThreadPool(processes=4)
results = thread_pool.map(redemption_thread, index_list)
for i in range(0, len(index_list) - 1):
    print(str(results[i]) + " rooz baraye namad " +
          my_sql.search.names(index_list[i]) + " zakhire shod")
    pass"""
"""index = "46348559193224090"
dataframe = redemption_thread(index)"""

"""for i in index_list:
    redemption_thread_pd(i)"""
#extract_save.black_list_check(index_list)
"""if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=3) as executor:
        results = executor.map(pfff, [0, 1, 2])
for r in results:
    print(r)"""
"""print(index_list)
MultiProcessing(index_list)"""

# my_sql.write.daily_operation_loop(dataframe_list, count_list)


"""print("Downloading time= " + str(((second_time - start_time).seconds / 60)))
print("second time= " + str(((third_time - second_time).seconds / 60)))
print("third time= " + str(((fourth_time - third_time).seconds / 60)))
print("fourth time= " + str(((end_time - fourth_time).seconds / 60)))"""
"""pool = ThreadPool(39)
darsad_taghir_gheymat = pool.map(extract_save.darsad_taghir_gheymat_initial, index_list)
pool.close()
pool.join()
print("Done")"""

"""def parameterMultiThread(self):
    # darydafte object asli namad
    tse_main_namad = tse_connect.namad(self)
    # daryafte parameter haye namad
    print(self)
    if tse_main_namad is not None:
        del tse_main_namad
        return tse_connect.parameter(tse_main_namad, self)
    else:
        del tse_main_namad
        return None
    pass"""

# pool multithread baraye daryafte list object namadhaye tse
"""pool = ThreadPool(59)
object_raw_list = pool.map(tse_connect.parameter, tse_object_list)
pool.close()
pool.join()
print(type(object_raw_list))
print(len(object_raw_list))"""

# bastane thread

# gereftane buge object_raw_list

"""
# tayine toole list namad
loop_length = len(object_raw_list)
print(loop_length)
for i in range(0, loop_length):
    # check kardane khali boodane namad va continue dar soorate khali boodan
    if object_raw_list[i] is None:
        print("skipping " + namadha_list[i])
        continue
    else:
        # sakhtane objecte asli namad_object
        # namad_object = tse_analize.listCalculate(object_raw_list[i], namadha_list[i])
        # save kardane paramterhaye namad_object dar database asli

        # Tarife Moteghayer ha
        # tarif moteghayerhaye controli loop
        six_month = int(tse_time.sixMonth())
        day_count = 0
        duplicate_date_count = 0
        row_save_count = 0

        # ge2reftane list date haye zakhire shode dar jadval namad
        saved_date_list = my_sql.log.list(namad_object.namad_entry)

        # tayine tool loop
        namad_object_length = len(namad_object.namad_date)
        # Payane tarif motheghayerha
        # loop zakhire sazi namad_object
        for day_count in range(0, 180):
            # check kardane inke az tool namad_object rad nashode bashe
            if day_count == (namad_object_length - 1):
                break
                pass
            # check kardane inke az 6 mah rad nashe
            elif int(namad_object.namad_date[day_count]) <= six_month:
                break
                pass
            # Check kardane vodoodi tekrari
            elif int(namad_object.namad_date[day_count]) in saved_date_list:
                duplicate_date_count += 1
                if duplicate_date_count < 10:
                    continue
                    pass
                else:
                    break
                    pass
                pass


            # save kardane voroodi dar database
            else:
                pass
            my_sql.write(namad_object, day_count)
            row_save_count += 1
            pass
        print(str(day_count) + " + " + str(row_save_count) + " rooz baraye namade " +
              namad_object.namad_entry + " save shod.")
        pass
    pass"""
