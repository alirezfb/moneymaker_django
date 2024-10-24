"""# -*- coding: utf-8 -*-
"""
in module baraye motasel shodan be tse va estekhraje
etelaat az oon tarahi shode
"""
import numpy

"""MARIADB COMMANDS
    SHOW STATUS WHERE `variable_name` = 'Threads_connected';
    kill USER username;
"""
import traceback
import mariadb
import pandas
from sqlalchemy import create_engine
import _sqlite3 as sql
import re
import logging
import os
import traceback
import sys
from threading import Thread
from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool
from time import sleep

import random
from multiprocessing import freeze_support
import pandas as pd


# START

class Write:

    def daily_operation_pd_2_old(index, index_list, pd_df):
        conn = mariadb.connect(
            user="root",
            password="Unique2213",
            host="localhost",
            port=3306,
            database="moneymaker"
        )
        """pd_df.drop(['priceChange', 'priceMin', 'priceMax', 'buy_I_Value',
                    'buy_N_Value', 'sell_I_Value', 'sell_N_Value',
                    'priceYesterday', 'priceFirst', 'last', 'id', 'insCode',
                    'iClose', 'yClose', 'pDrCotVal', 'recDate', 'hEven'], axis=1, inplace=True)"""
        cur = conn.cursor()
        namad_symbol = "nmd" + str(index)
        date_list = search.dates(index)
        row_save_count = 0
        duplicate_date_count: int = 0
        duplicate_check = False
        engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306/moneymaker")
        row_save_count = pd_df.to_sql(name=namad_symbol, con=engine, if_exists='append', index=False)
        for count in index_list:
            error_count = 0
            error_message = ""
            while error_count < 3:
                try:
                    if pd_df.loc[0, 'dEven'] in date_list:
                        duplicate_check = True
                        error_message = "duplicate date"
                        break
                    else:
                        duplicate_check = False
                        cur.execute(("INSERT INTO %s ("
                                     "date,"
                                     "kharid_haghighi,"
                                     "hajm_kharid_haghighi,"
                                     "foroosh_haghighi,"
                                     "hajm_foroosh_haghighi,"
                                     "kharid_hoghooghi,"
                                     "hajm_kharid_hoghooghi,"
                                     "foroosh_hoghooghi,"
                                     "hajm_foroosh_hoghooghi,"
                                     "ghodrat_kharid_haghighi,"
                                     "ghodrat_foroosh_haghighi,"
                                     "ghodrat_kharid_hoghooghi,"
                                     "ghodrat_foroosh_hoghooghi,"
                                     "kharid_haghighi_hoghooghi,"
                                     "hajm_kharid_haghighi_hoghooghi,"
                                     "foroosh_haghighi_hoghooghi,"
                                     "hajm_foroosh_haghighi_hoghooghi,"
                                     "percentage,"
                                     "adj_close_price,"
                                     "tedad_moamelat,"
                                     "volume,"
                                     "namad_value"
                                     ")"
                                     "VALUES('%s', '%s', '%s', '%s', '%s',"
                                     "'%s', '%s', '%s', '%s', '%s', '%s','%s',"
                                     "'%s' , '%s', '%s', '%s', '%s', '%s','%s',"
                                     "'%s','%s', '%s' )"
                                     % (namad_symbol,
                                        pd_df.loc[count, 'dEven'],
                                        pd_df.loc[count, 'buy_I_Count'],
                                        pd_df.loc[count, 'buy_I_Volume'],
                                        pd_df.loc[count, 'sell_I_Count'],
                                        pd_df.loc[count, 'sell_I_Volume'],
                                        pd_df.loc[count, 'buy_N_Count'],
                                        pd_df.loc[count, 'buy_N_Volume'],
                                        pd_df.loc[count, 'sell_N_Count'],
                                        pd_df.loc[count, 'sell_N_Volume'],
                                        pd_df.loc[count, 'ghodrat_kh_ha'],
                                        pd_df.loc[count, 'ghodrat_fo_ha'],
                                        pd_df.loc[count, 'ghodrat_kh_ho'],
                                        pd_df.loc[count, 'ghodrat_fo_ho'],
                                        pd_df.loc[count, 'ghodrat_khha_khho'],
                                        pd_df.loc[count, 'ghodrat_hjmkhha_hjmkhho'],
                                        pd_df.loc[count, 'ghodrat_foha_foho'],
                                        pd_df.loc[count, 'ghodrat_hjmfoha_hjmfoho'],
                                        pd_df.loc[count, 'percentage'],
                                        pd_df.loc[count, 'pClosing'],
                                        pd_df.loc[count, 'zTotTran'],
                                        pd_df.loc[count, 'qTotTran5J'],
                                        pd_df.loc[count, 'qTotCap']
                                        )).replace("'", " "))
                        row_save_count += 1
                        conn.commit()
                        break
                        pass
                    pass
                except:
                    error_count += 1
                    log.error_write(index)
                    pass
                pass
            if error_count >= 3 or duplicate_check is True:
                if duplicate_date_count % 4 == 0:
                    pass
                else:
                    pass
                if duplicate_date_count > 15:
                    break
                    pass
                else:
                    duplicate_date_count += 1
                    pass
            else:
                pass
            pass
        conn.commit()
        conn.close()
        return row_save_count

    def HistoryMoneymaker(original_dataframe: pandas.DataFrame, index, tbl_dates: list = None):
        # making a copy out of the original dataframe to protect form changes
        dataframe = original_dataframe.copy(deep=False)
        for i in range(0, 2):
            try:
                # error check variable
                error_check = False
                # dropping inscode
                dataframe.drop(['insCode'], axis=1, inplace=True)
                # creating namad_symbol
                namad_symbol = "nmd" + str(index)
                # checking if the table exists and create it if not
                HistoryTableCreate.price_table(index)
                row_save_count = 0
                # connecting to database
                engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306/moneymaker")

                # adding to database
                if tbl_dates is not None and error_check is False:
                    # declaring variables
                    loop_check = True
                    counter = 0
                    last_saved_date = tbl_dates[0]
                    # checking if there's any last dates saved and list length
                    if tbl_dates[0] != 0 and len(tbl_dates) > 0:
                        # finding columns that needs to be saved
                        while loop_check is True:
                            if last_saved_date >= dataframe.loc[counter, 'dEven']:
                                loop_check = False
                                pass
                            elif counter > 299:
                                loop_check = False
                                pass
                            else:
                                counter += 1
                                pass
                            pass
                        # saving to database
                        if counter < 1:
                            # for when there isn't any existing records in db
                            row_save_count = dataframe.to_sql(name=namad_symbol, con=engine,
                                                              if_exists='append', index=False)
                            pass
                        else:
                            """for when there are some records in db and
                                to sql function saves only columns that
                                are not saved"""
                            dataframe.drop(dataframe.index[counter:], axis=0, inplace=True)
                            row_save_count = dataframe.to_sql(name=namad_symbol, con=engine,
                                                              if_exists='append', index=False)
                            pass
                        pass
                    else:
                        counter = dataframe.to_sql(name=namad_symbol, con=engine,
                                                   if_exists='append', index=False, chunksize=1)
                        pass
                # there was an error and data needs to be saved in static form
                elif search.table(index=index) is True:
                    counter = dataframe.to_sql(name=namad_symbol, con=engine,
                                               if_exists='append', index=False,
                                               chunksize=1)
                else:
                    counter = dataframe.to_sql(name=namad_symbol, con=engine,
                                               if_exists='append', index=False)
                    pass
                # killing the engine
                engine.dispose()
                del engine
                # return saved entries
                return counter
            except:
                error_check = True
                if i == 0:
                    dataframe = original_dataframe.copy(deep=False)
                    dataframe.fillna(0)
                    pass
                else:
                    try:
                        engine.dispose()
                        del engine
                        pass
                    except:
                        pass
                    log.error_write(index)
                    return 0
                    pass
                pass
            pass
        pass

    def LiveSchema(dataframe: pandas.DataFrame, analyze: bool, index, tbl_dates: list = None):
        # making a copy out of the original dataframe to protect form changes
        for i in range(0, 2):
            try:
                # creating namad_symbol
                namad_symbol = "nmd" + str(index)
                # checking if the table exists and create it if not and create database engine
                if analyze is True:
                    row_save_count = 0
                    engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306"
                                           "/live_analyze_update")
                    pass
                else:
                    engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306"
                                           "/live_moneymaker_update")
                    pass
                # adding to database
                counter = dataframe.to_sql(name=namad_symbol, con=engine,
                                           if_exists='append', index=False)
                # killing the engine
                engine.dispose()
                del engine
                # return saved entries
                return counter
            except:
                if i == 0:
                    dataframe.fillna(0)
                    pass
                else:
                    try:
                        engine.dispose()
                        del engine
                        pass
                    except:
                        pass
                    log.error_write(index)
                    return 0
                    pass

    def all_best_limits(dataframe: pandas.DataFrame, live=False, truncate=True):
        for i in range(0, 2):
            try:
                if live is True:
                    tbl_name = "live_best_limits"
                else:
                    tbl_name = "all_best_limits"
                # checking if the table exists and create it if not and create database engine
                engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306"
                                       "/best_limits")
                # adding to database
                if truncate is True:
                    modification.truncate("best_limits", tbl_name)
                else:
                    pass
                counter = dataframe.to_sql(name=tbl_name, con=engine,
                                           if_exists='append', index=False)
                # killing the engine
                engine.dispose()
                del engine
                # return saved entries
                return counter
            except:

                try:
                    engine.dispose()
                    del engine
                    pass
                except:
                    pass
                log.error_write("")
                return 0
                pass

    def live_best_limits(index, dataframe: pandas.DataFrame):
        for i in range(0, 2):
            try:
                # creating namad_symbol
                namad_symbol = "nmd" + str(index)
                # checking if the table exists and create it if not and create database engine
                engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306"
                                       "/best_limits")
                # adding to database
                counter = dataframe.to_sql(name=namad_symbol, con=engine,
                                           if_exists='append', index=False)
                # killing the engine
                engine.dispose()
                del engine
                # return saved entries
                return counter
            except:
                if i == 0:
                    dataframe.fillna(0)
                    pass
                else:
                    try:
                        engine.dispose()
                        del engine
                        pass
                    except:
                        pass
                    log.error_write(index)
                    return 0
                    pass

    def close_best_limits(index, dataframe: pandas.DataFrame):
        for i in range(0, 2):
            try:
                # creating namad_symbol
                namad_symbol = "nmd" + str(index)
                # checking if the table exists and create it if not and create database engine
                engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306"
                                       "/close_best_limits")
                # adding to database
                counter = dataframe.to_sql(name=namad_symbol, con=engine,
                                           if_exists='append', index=False)
                # killing the engine
                engine.dispose()
                del engine
                # return saved entries
                return counter
            except:
                if i == 0:
                    dataframe.fillna(0)
                    pass
                else:
                    try:
                        engine.dispose()
                        del engine
                        pass
                    except:
                        pass
                    log.error_write(index)
                    return 0
                    pass

    def analize_list_daily(original_dataframe: pandas.DataFrame, index, tbl_dates: list = None):
        # creating dummpy engine
        for i in range(0, 2):
            try:
                dataframe = original_dataframe.copy(deep=False)
                # error check variable
                error_check = False
                # generate index number and table name
                index = dataframe.loc[0, 'insCode']
                namad_symbol = "nmd" + str(index)
                # dropping inscode
                dataframe.drop(['insCode'], axis=1, inplace=True)
                # checking if the table exists and create it if not
                HistoryTableCreate.analize_table(index)
                row_save_count = 0
                engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306/analize")
                # checking if tbl_dates exists or error_check is False, and it's not the second time running this loop
                if tbl_dates is not None and error_check is False:
                    # declaring variables
                    loop_check = True
                    counter = 0
                    last_saved_date = tbl_dates[0]
                    # checking if there's any last dates saved and list length
                    if tbl_dates[0] != 0 and len(tbl_dates) > 0:
                        # finding columns that needs to be saved
                        while loop_check is True:
                            if last_saved_date >= dataframe.loc[counter, 'dEven']:
                                loop_check = False
                                pass
                            elif counter > 299:
                                loop_check = False
                                pass
                            else:
                                counter += 1
                                pass
                            pass
                        if counter < 1:
                            # for when there isn't any existing records in db
                            row_save_count = dataframe.to_sql(name=namad_symbol, con=engine,
                                                              if_exists='append', index=False)
                            pass
                        else:
                            """for when there are some records in db and
                                to sql function saves only columns that
                                are not saved"""
                            dataframe.drop(dataframe.index[counter:], axis=0, inplace=True)
                            row_save_count = dataframe.to_sql(name=namad_symbol, con=engine,
                                                              if_exists='append', index=False)
                            pass
                        pass
                    else:
                        counter = dataframe.to_sql(name=namad_symbol, con=engine,
                                                   if_exists='append', index=False)
                        pass
                # there was an error and data needs to be saved in static form
                else:
                    counter = dataframe.to_sql(name=namad_symbol, con=engine,
                                               if_exists='append', index=False)
                    pass
                # killing the engine
                engine.dispose()
                del engine
                # return saved entries
                return counter
            except:
                error_check = True
                if i == 0:
                    dataframe.fillna(0)
                    pass
                else:
                    try:
                        engine.dispose()
                        del engine
                        pass
                    except:
                        pass
                    log.error_write(index)
                    return 0
                    pass
                pass
            pass
        pass

    def tblnamadha_update(self: pandas.DataFrame):
        try:
            if self is None:
                return None
            else:
                """loop length"""
                loop_length = self.shape[0]
                pass
            # getting index list
            index_list = search.any_table_records("0", "tblnamadha", "namad_index", "manager")
            self.drop(['customLabel', 'dEven', 'hEven',
                       'pClosing', 'pDrCotVal', 'zTotTran',
                       'qTotTran5J', 'qTotCap', 'priceYesterday',
                       'percent', 'priceChangePercent', 'hEvenShow',
                       'color', 'fontSize', 'fontColor'], axis=1, inplace=True)
            self.rename(columns={"insCode": "namad_index"}, inplace=True)
            self.rename(columns={"lVal18AFC": "name"}, inplace=True)
            self.rename(columns={"lVal30": "full_name"}, inplace=True)
            self.rename(columns={"lSecVal": "category"}, inplace=True)
            dic: dict = {
                "namad_index": [],
                "name": [],
                "full_name": [],
                "category": [],
            }
            new_df = pandas.DataFrame()
            for i in range(0, loop_length):
                df_series = self.loc[i]
                # index check
                if df_series.loc['namad_index'] not in index_list:
                    dic["namad_index"].append(df_series.loc['namad_index'])
                    dic["name"].append(df_series.loc['name'])
                    dic["full_name"].append(df_series.loc['full_name'])
                    dic["category"].append(df_series.loc['category'])
                    pass
                else:
                    pass
                pass
            # connecting to database
            engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306/manager")
            if len(dic) != 0:
                row_save_count = new_df.to_sql(name="tblnamadha", con=engine,
                                               if_exists='append', index=False)
                pass
            else:
                pass
        except:
            print(sys.exc_info())
            log.error_write("0")
            return 0


class binance_object:
    def __init__(self):
        pass

    class chart_data:
        def __init__(self):
            self.date_field = 'open_time'
            self.obj_type = 'cryptocurrency'
            self.df_schema = 'crypto_chart_data'


def write_anything(org_dataframe, tbl_name, obj, existing_dates=None):
    # making a copy out of the original dataframe to protect form changes
    dataframe = org_dataframe.copy(deep=False)
    schema = obj.df_schema
    date_field = obj.date_field
    for i in range(0, 2):
        try:
            # error check variable
            error_check = False
            # checking if the table exists and create it if not
            #HistoryTableCreate.price_table(index)
            row_save_count = 0
            # connecting to database
            engine = create_engine("mariadb+mariadbconnector://" +
                                   "root:Unique2213@127.0.0.1:3306/" +
                                   schema)
            # adding to database
            if existing_dates is not None and error_check is False:
                # declaring variables
                loop_check = True
                loop_counter = 0
                last_saved_date = existing_dates[0]
                # checking if there's any last dates saved and list length
                if existing_dates[0] != 0 and len(existing_dates) > 0:
                    # finding columns that needs to be saved
                    while loop_check is True:
                        if last_saved_date >= dataframe.loc[loop_counter, date_field]:
                            loop_check = False
                            pass
                        elif loop_counter > 299:
                            loop_check = False
                            pass
                        else:
                            loop_counter += 1
                            pass
                        pass
                    # saving to database
                    if loop_counter < 1:
                        # for when there isn't any existing records in db
                        row_save_count = dataframe.to_sql(name=tbl_name, con=engine,
                                                          if_exists='append', index=False)
                        pass
                    else:
                        """for when there are some records in db and
                            to sql function saves only columns that
                            are not saved"""
                        dataframe.drop(dataframe.index[loop_counter:], axis=0, inplace=True)
                        row_save_count = dataframe.to_sql(name=tbl_name, con=engine,
                                                          if_exists='append', index=False)
                        pass
                    pass
                else:
                    loop_counter = dataframe.to_sql(name=tbl_name, con=engine,
                                               if_exists='append', index=False, chunksize=1)
                    pass
            # there was an error and data needs to be saved in static form
            #elif search.table(index=index) is True:
            #counter = dataframe.to_sql(name=namad_symbol, con=engine,
            #if_exists='append', index=False,
            #chunksize=1)
            else:
                loop_counter = dataframe.to_sql(name=tbl_name, con=engine,
                                           if_exists='append', index=False)
                pass
            # killing the engine
            engine.dispose()
            del engine
            # return saved entries
            return loop_counter
        except:
            error_check = True
            if i == 0:
                dataframe = org_dataframe.copy(deep=False)
                dataframe.fillna(0)
                pass
            else:
                try:
                    engine.dispose()
                    del engine
                    pass
                except:
                    pass
                log.error_write(tbl_name)
                return 0
                pass
            pass
        pass
    pass


class modification:

    def truncate(schema, tbl_name):
        try:
            script = "truncate table " + tbl_name
            # baz kardane sql va khandane tblnamadhatemp
            conn = mariadb.connect(
                user="root",
                password="Unique2213",
                host="localhost",
                port=3306,
                database=schema
            )
            cur = conn.cursor()
            cur.execute(script)
            conn.commit()
            conn.close()
            del conn
            return True
        except:
            try:
                conn.commit()
                conn.close()
                del conn
            except:
                pass
            log.error_write(search.index(''))
            return False
        pass

    def drop(index, address):
        namad_symbol = search.names(index)
        existance = search.table(table_name=namad_symbol)
        if existance is False:
            return None
        else:
            error_count = 0
            while error_count < 5:
                try:
                    con = sql.connect(address, check_same_thread=False)
                    cur = con.cursor()
                    cur.execute("DROP TABLE '%s'"
                                % namad_symbol)
                    con.commit()
                    con.close()
                    return None
                except:
                    error_count += 1
                    sleep(random.random())
                    pass
                pass
            if error_count > 4:
                log.error_write(namad_symbol)
                pass
            else:
                pass
            return None
        pass


class read_temp:

    def closing_price(index, index_number):
        namad_symbol = search.names(index)
        error_count = 0
        while error_count < 3:
            try:
                # baz kardane sql va khandane tblnamadha
                con = sql.connect(locator.temp_database(), check_same_thread=False)
                con = sql.connect(locator.temp_database(), check_same_thread=False)
                cur = con.cursor()
                if index_number > 0:
                    command = "SELECT dEven, pClosing, zTotTran, qTotTran5J, qTotCap FROM '%s' WHERE ROWID = '%s'"
                    result = cur.execute(command
                                         % (namad_symbol, index_number))
                    pass
                else:
                    command = "SELECT dEven, pClosing, zTotTran, qTotTran5J, qTotCap FROM '%s'"
                    result = cur.execute(command
                                         % namad_symbol)
                result = result.fetchall()
                con.commit()
                con.close()
                if index_number > 0:
                    return result[0]
                else:
                    return result
            except:
                error_count += 1
                sleep(random.random())
                if error_count >= 3:
                    log.error_write(namad_symbol)
                    return None
                else:
                    pass
                pass
            pass
        pass

    def closing_price_pd(index, index_number):
        namad_symbol = search.names(index)
        error_count = 0
        result = None
        while error_count < 3:
            try:
                # baz kardane sql va khandane tblnamadha
                con = sql.connect(locator.temp_database(), check_same_thread=False)
                cur = con.cursor()
                if index_number > 0:
                    query = "SELECT dEven, pClosing, zTotTran, qTotTran5J, qTotCap" \
                            " FROM " + namad_symbol + " WHERE ROWID = " + index_number
                    pass
                else:
                    query = "SELECT dEven, pClosing, zTotTran, qTotTran5J, qTotCap FROM " + namad_symbol
                    pass
                result = pd.read_sql(query, con)
                con.commit()
                con.close()
                return result
            except:
                if error_count >= 3:
                    log.error_write(namad_symbol)
                else:
                    error_count += 1
                    sleep(random.random())
                    pass
                pass
            return result
        pass

    def client_types(index, index_number):
        namad_symbol = search.names(index)
        error_count = 0
        while error_count < 3:
            try:
                # baz kardane sql va khandane tblnamadha
                con = sql.connect(locator.temp_database(), check_same_thread=False)
                cur = con.cursor()
                if index_number > 0:
                    result = cur.execute(r"SELECT buy_I_Count,"
                                         r"buy_I_Volume,"
                                         r" sell_I_Count,"
                                         r" sell_I_Volume,"
                                         r" buy_N_Count,"
                                         r" buy_N_Volume,"
                                         r" sell_N_Count,"
                                         r" sell_N_Volume"
                                         r" FROM '%s' WHERE ROWID = '%s'"
                                         % (namad_symbol, index_number))
                    pass
                else:
                    result = cur.execute(r"SELECT buy_I_Count,"
                                         r"buy_I_Volume,"
                                         r" sell_I_Count,"
                                         r" sell_I_Volume,"
                                         r" buy_N_Count,"
                                         r" buy_N_Volume,"
                                         r" sell_N_Count,"
                                         r" sell_N_Volume"
                                         r" FROM '%s'"
                                         % namad_symbol)
                result = result.fetchall()
                con.commit()
                con.close()
                break
            except:
                error_count += 1
                log.error_write(namad_symbol)
                pass
            pass
        if error_count < 3:
            del cur, con, index, namad_symbol
            return result
        else:
            log.error_write(namad_symbol)
            return None
        pass

    def client_types_pd(index, index_number):
        namad_symbol = search.names(index)
        error_count = 0
        while error_count < 3:
            try:
                # baz kardane sql va khandane tblnamadha
                con = sql.connect(locator.temp_database(), check_same_thread=False)
                cur = con.cursor()
                if index_number > 0:
                    query = "SELECT buy_I_Count," \
                            "buy_I_Volume," \
                            " sell_I_Count," \
                            " sell_I_Volume," \
                            " buy_N_Count," \
                            " buy_N_Volume," \
                            " sell_N_Count," \
                            " sell_N_Volume" \
                            " FROM " + namad_symbol + "WHERE ROWID = " + index_number
                    pass
                else:
                    query = "SELECT buy_I_Count," \
                            " sell_I_Count," \
                            "buy_I_Volume," \
                            " sell_I_Volume," \
                            " buy_N_Count," \
                            " buy_N_Volume," \
                            " sell_N_Count," \
                            " sell_N_Volume" \
                            " FROM " + namad_symbol
                result = pd.read_sql(query, con)
                con.commit()
                con.close()
                break
            except:
                error_count += 1
                log.error_write(namad_symbol)
                pass
            pass
        if error_count < 3:
            del cur, con, index, namad_symbol
            return result
        else:
            log.error_write(namad_symbol)
            return None
        pass

    def tse_analize(index, index_number):
        namad_symbol = search.names(index)
        error_count = 0
        while error_count < 3:
            try:
                # baz kardane sql va khandane tblnamadha
                con = sql.connect(locator.temp_database(), check_same_thread=False)
                cur = con.cursor()
                if index_number > 0:
                    result = cur.execute(r"SELECT ghodrat_kh_ha,"
                                         r"ghodrat_fo_ha,"
                                         r"ghodrat_kh_ho,"
                                         r"ghodrat_fo_ho,"
                                         r"ghodrat_khha_khho,"
                                         r"ghodrat_hjmkhha_hjmkhho,"
                                         r"ghodrat_foha_foho,"
                                         r"ghodrat_hjmfoha_hjmfoho,"
                                         r"percentage"
                                         r" FROM '%s'"
                                         r"WHERE ROWID = '%s'"
                                         % (namad_symbol, index_number))
                    pass
                else:
                    result = cur.execute(r"SELECT ghodrat_kh_ha,"
                                         r"ghodrat_fo_ha,"
                                         r"ghodrat_kh_ho,"
                                         r"ghodrat_fo_ho,"
                                         r"ghodrat_khha_khho,"
                                         r"ghodrat_hjmkhha_hjmkhho,"
                                         r"ghodrat_foha_foho,"
                                         r"ghodrat_hjmfoha_hjmfoho,"
                                         r"percentage"
                                         r" FROM '%s'"
                                         % namad_symbol)
                result = result.fetchall()
                con.commit()
                con.close()
                break
            except:
                error_count += 1
                log.error_write(namad_symbol)
                pass
            pass
        if error_count < 3:
            del cur, con, index, namad_symbol
            return result
        else:
            print("Error reading closing price from temp table for: " + namad_symbol)
            return None
        pass

    def all(index, index_number):
        namad_symbol = search.names(index)
        error_count = 0
        while error_count < 3:
            try:
                # baz kardane sql va khandane tblnamadha
                con = sql.connect(locator.temp_database(), check_same_thread=False)
                cur = con.cursor()
                if index_number > 0:
                    result = cur.execute(r"SELECT * "
                                         r"FROM '%s'"
                                         r"WHERE ROWID = '%s'"
                                         % (namad_symbol, index_number))
                    pass
                else:
                    result = cur.execute(r"SELECT * "
                                         r"FROM '%s'"
                                         % namad_symbol)
                result = result.fetchall()
                con.commit()
                con.close()
                break
            except:
                error_count += 1
                log.error_write(namad_symbol)
                pass
            pass
        if error_count < 3:
            return result
        else:
            print("Error reading all data from temp database table for: " + namad_symbol)
            return None
        pass

    def all_pd(index, index_number):
        namad_symbol = search.names(index)
        error_count = 0
        result = None
        while error_count < 3:
            try:
                # baz kardane sql va khandane tblnamadha
                con = sql.connect(locator.temp_database(), check_same_thread=False)
                cur = con.cursor()
                if index_number > 0:
                    query = "SELECT * FROM " + namad_symbol + " WHERE ROWID = " + index_number
                    pass
                else:
                    query = "SELECT * FROM " + namad_symbol
                result = pd.read_sql(query, con)
                con.commit()
                con.close()
                break
            except:
                error_count += 1
                log.error_write(namad_symbol)
                pass
            pass
        if error_count < 3:
            return result
        else:
            print("Error reading all data from temp database table for: " + namad_symbol)
            return result
        pass


class read:
    """
    in function baraye khandan va bargardane
    nam namad ha az table tblonamadha hastesh
    """

    @staticmethod
    def names():
        error_count = 0
        while error_count < 3:
            try:
                # baz kardane sql va khandane tblnamadha
                conn = mariadb.connect(
                    user="root",
                    password="Unique2213",
                    host="localhost",
                    port=3306,
                    database="manager"
                )
                cur = conn.cursor()
                cur.execute(r"SELECT name FROM tblnamadha")
                conn.commit()
                conn.close()
                del conn
                # loop baraye estekhraj kardane esme namadha
                namadha = []
                for i in cur:
                    namadha.append(i[0])
                    pass
                return namadha
            except:
                try:
                    conn.commit()
                    conn.close()
                    del conn
                    pass
                except:
                    pass
                error_count += 1
                log.error_write("")
                pass
            pass
        # return if error occured
        return None

    def index(bl_check=False):
        try:
            # baz kardane sql va khandane tblnamadhatemp
            conn = mariadb.connect(
                user="root",
                password="Unique2213",
                host="localhost",
                port=3306,
                database="manager"
            )
            cur = conn.cursor()
            cur.execute(r"SELECT namad_index FROM tblnamadha")
            conn.commit()
            conn.close()
            del conn
            if bl_check is True:
                blacklist = black_list.read()
                pass
            else:
                blacklist = []
            # loop baraye estekhraj kardane index namadha
            namadha_index = []
            if cur.fetchone() is None:
                return None
            for i in cur:
                if i[0] in blacklist:
                    continue
                else:
                    namadha_index.append(i[0])
                pass
            return namadha_index
        except:
            try:
                conn.commit()
                conn.close()
                del conn
                pass
            except:
                pass
            log.error_write("")

    def temp_table(index):
        namad_symbol = search.names(index)
        con = sql.connect(locator.temp_database(), check_same_thread=False)
        cur = con.cursor()
        result = cur.execute(r"SELECT * FROM '%s'"
                             % namad_symbol)
        result = result.fetchall()
        con.commit()
        con.close()
        # loop baraye estekhraj kardane index namadha
        namadha_index = []
        for i in result:
            namadha_index.append(i[0])
            pass
        return namadha_index

    """def analize_list(self):"""

    def all_tables(index, schema):
        try:
            # generating table name
            namad_symbol = "nmd" + str(index)
            script = 'SELECT * FROM ' + namad_symbol + ' LIMIT 100'
            # creating database connection string
            connecion_string = "mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306/" + schema
            # connecting to database
            engine = create_engine(connecion_string)
            data = pd.read_sql(script, engine)
            engine.dispose()
            del engine
            return data
        except:
            try:
                engine.dispose()
                del engine
                pass
            except:
                pass
            log.error_write(index)
            return None


class count:

    def rows(address, table_name=None, index=None):
        if table_name is None:
            table_name = search.names(index)
            pass
        else:
            pass
        error_count = 0
        while error_count < 7:
            try:
                con = sql.connect(address, check_same_thread=False)
                cur = con.cursor()
                result = cur.execute(r"SELECT count(*) FROM %s"
                                     % table_name)
                result = result.fetchall()
                con.commit()
                con.close()
                return result[0][0]
            except:
                error_count += 1
                sleep(random.random())
                if error_count >= 7:
                    log.error_write(table_name)
                    return 0
                    pass
                else:
                    pass


class search:

    def script(schema: str, script: str, df_return=True):
        try:
            if df_return is True:
                engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306"
                                       "/" + schema)

                return_object = pd.read_sql(script, engine)
                engine.dispose()
                del engine
                pass
            else:
                # baz kardane sql va khandane tblnamadhatemp
                conn = mariadb.connect(
                    user="root",
                    password="Unique2213",
                    host="localhost",
                    port=3306,
                    database=schema
                )
                cur = conn.cursor()
                cur.execute(script)
                conn.commit()
                conn.close()
                del conn
                try:
                    return_object = cur.fetchall()
                except:
                    return_object = []
            return return_object
        except:
            try:
                if df_return is True:
                    engine.dispose()
                    del engine
                else:
                    conn.commit()
                    conn.close()
                    del conn
                pass
            except:
                pass
            log.error_write(search.index(''))
            return None
        pass

    def any_table_records(namad_index, table_name, selected_index, schema, searched_item=None, searched_index=None):
        error_count = 0
        while error_count < 7:
            try:
                # baz kardane sql va khandane tblnamadhatemp
                conn = mariadb.connect(
                    user="root",
                    password="Unique2213",
                    host="localhost",
                    port=3306,
                    database=schema
                )
                cur = conn.cursor()
                if searched_index or searched_item is None:
                    cur.execute(("SELECT %s FROM %s"
                                 % (selected_index, table_name)))
                else:
                    cur.execute(("SELECT %s FROM %s WHERE %s LIKE %s"
                                 % (selected_index, table_name, searched_index, searched_item)))
                conn.commit()
                conn.close()
                del conn
                temp = cur.fetchall()
                result = []
                for i in temp:
                    result.append(i[0])
                    pass
                return result
            except:
                try:
                    conn.commit()
                    conn.close()
                    del conn
                    pass
                except:
                    pass
                error_count += 1
                sleep(random.random())
                if error_count >= 7:
                    log.error_write(search.index(namad_index))
                    return None
                    pass
                else:
                    pass
                pass
            return None
        pass

    def names(self):
        try:
            # baz kardane sql va khandane tblnamadhatemp
            conn = mariadb.connect(
                user="root",
                password="Unique2213",
                host="localhost",
                port=3306,
                database="manager"
            )
            cur = conn.cursor()
            cur.execute(("SELECT name FROM tblnamadha WHERE namad_index LIKE %s"
                         % (self)))
            conn.commit()
            conn.close()
            del conn
            result = cur.fetchone()[0]
            return result
        except:
            try:
                conn.commit()
                conn.close()
                del conn
                pass
            except:
                pass
            log.error_write(search.index(self))
            return None
        pass

    def table(table_name: str = None, index=None, schema: str = None):
        if table_name is None:
            table_name = "nmd" + str(index)
            pass
        else:
            pass
        if schema is None:
            schema = "moneymaker"
            pass
        else:
            pass
        try:
            # baz kardane sql va khandane tblnamadhatemp
            conn = mariadb.connect(
                user="root",
                password="Unique2213",
                host="localhost",
                port=3306,
                database=schema
            )
            cur = conn.cursor()
            cur.execute(("SHOW TABLES FROM %s LIKE '%s'"
                         % (schema,
                            table_name)))
            conn.commit()
            conn.close()
            del conn
            if cur.fetchone() is None:
                return False
            else:
                return True
        except:
            try:
                conn.commit()
                conn.close()
                del conn
                pass
            except:
                pass
            log.error_write(search.index(table_name))
            return None

    def index(self):
        try:
            # baz kardane sql va khandane tblnamadhatemp
            conn = mariadb.connect(
                user="root",
                password="Unique2213",
                host="localhost",
                port=3306,
                database="manager"
            )
            cur = conn.cursor()
            result = cur.execute(r"SELECT namad_index FROM tblnamadha WHERE name LIKE '%s'"
                                 % (self))
            result = result.fetchone()
            conn.commit()
            conn.close()
            del conn
            result = result[0]
            return result
        except:
            try:
                conn.commit()
                conn.close()
                del conn
                pass
            except:
                pass
            log.error_write(self)
            return None
        pass

    def dates(index, schema: str = None):
        if search.table(index=index) is not True:
            return [0]
        elif schema is None:
            schema = "moneymaker"
            pass
        else:
            pass
        table_name = "nmd" + str(index)
        try:
            # baz kardane sql va khandane tblnamadhatemp
            conn = mariadb.connect(
                user="root",
                password="Unique2213",
                host="localhost",
                port=3306,
                database=schema
            )
            cur = conn.cursor()
            cur.execute(r"SELECT dEven FROM  %s "
                        % (table_name))
            q_result = cur.fetchall()
            conn.commit()
            conn.close()
            del conn
            if q_result is None or len(q_result) == 0:
                return [0]
            else:
                return_list = []
                if schema == "analize":
                    for i in reversed(q_result):
                        return_list.append(int(i[0]))
                        pass
                    pass
                else:
                    for i in reversed(q_result):
                        return_list.append(int(i[0]))
                        pass
                    pass
                return return_list
                pass
        except:
            try:
                conn.commit()
                conn.close()
                del conn
                pass
            except:
                pass
            log.error_write(search.names(index))
            return [0]
        pass


class check:
    def duplicate_date(index):
        try:
            closing_price_list = read_temp.closing_price(index, 0)
            date_list = search.dates(search.names(index))
            duplicate_counter = 0
            unique_counter = 0
            for i in closing_price_list:
                if i[0] in date_list:
                    duplicate_counter += 1
                    pass
                else:
                    unique_counter += 1
                    break
                    pass
                if duplicate_counter > 15:
                    break
                    pass
                else:
                    pass
                pass
            #True if it's duplicate and there is no unique date
            if duplicate_counter > 15 and unique_counter < 1:
                return True
            #False if it's not duplicate or there is a unique date
            else:
                return False
            pass
        except:
            log.error_write(search.names(index))

    def duplicate_date_pd(dataframe):
        try:
            closing_price_list = dataframe.loc[:, 'dEven']
            index = dataframe.loc[0, 'insCode']
            date_list = search.dates(search.names(index))
            duplicate_counter = 0
            unique_counter = 0
            for i in closing_price_list:
                if str(i) in date_list:
                    duplicate_counter += 1
                    pass
                else:
                    unique_counter += 1
                    break
                    pass
                if duplicate_counter > 15:
                    break
                    pass
                else:
                    pass
                pass
            #True if it's duplicate and there is no unique date
            if duplicate_counter > 15 and unique_counter < 1:
                return True
            #False if it's not duplicate or there is a unique date
            else:
                return False
            pass
        except:
            log.error_write(index)


"""
in tabe baraye khandane nam haye namadha az table namad
va sakhtane tabali jodagane baraye harkodoom az namad ha
tarahi shode"""


def row_counter(database, table_name):
    error_count = 0
    error_message = ""
    result = None
    while error_count < 3:
        try:
            # baz kardane sql va khandane tblnamadha
            con = sql.connect(database, check_same_thread=False)
            cur = con.cursor()
            result = cur.execute(r"SELECT COUNT(*) FROM '%s'"
                                 % table_name)
            result = result.fetchall()
            con.commit()
            con.close()
            break
        except:
            error_count += 1
            sleep(random.random())
            if error_count >= 3:
                log.error_write(table_name)
                return None
                pass
            else:
                pass
            pass
        pass
    del cur, con, table_name
    return result[0][0]


def percentage_update_table():
    index_list = read.index()
    namad_list = []
    for i in index_list:
        namad_list.append(search.names(i))
        pass
    for i in namad_list:
        try:
            con = sql.connect(locator.database(), check_same_thread=False)
            cur = con.cursor()
            con.execute("ALTER TABLE '%s'"
                        "ADD percentage integer"
                        % (i))
            con.commit()
            con.close()
            print('succes')
            pass

        except:
            log.error_write(i)
            sleep(random.random())
            pass
        pass
    return "Done"


def close_price_update_table():
    index_list = read.index()
    namad_list = []
    for i in index_list:
        namad_list.append(search.names(i))
        pass
    for i in namad_list:
        error_count = 0
        while error_count < 7:
            try:
                con = sql.connect(locator.database(), check_same_thread=False)
                cur = con.cursor()
                con.execute("ALTER TABLE '%s'"
                            "ADD close_price integer"
                            % (i))
                con.commit()
                con.close()
                print(i + ' creating success.')
                pass

            except:
                error_count += 1
                log.error_write(i)
                sleep(random.uniform(0.1, 20.5))
                pass
            pass
        pass
    return "Done"


class HistoryTableCreate:
    def price_table(self=None):
        try:
            # self is symbol's index
            if self is None:
                index_list = read.index()
                pass
            else:
                index_list = [self]
            conn = mariadb.connect(
                user="root",
                password="Unique2213",
                host="localhost",
                port=3306,
                database="moneymaker"
            )
            for i in index_list:
                if search.table(index=i) is False:
                    try:
                        name = "nmd" + str(i)
                        cur = conn.cursor()
                        cur.execute("CREATE TABLE IF NOT EXISTS %s ("
                                    "dEven varchar(20) UNIQUE NOT NULL PRIMARY KEY,"
                                    "buy_I_Count varchar(20) NOT NULL,"
                                    "buy_I_Volume varchar(20) NOT NULL,"
                                    "sell_I_Count varchar(20) NOT NULL,"
                                    "sell_I_Volume varchar(20) NOT NULL,"
                                    "buy_N_Count varchar(20) NOT NULL,"
                                    "buy_N_Volume varchar(20) NOT NULL,"
                                    "sell_N_Count varchar(20) NOT NULL,"
                                    "sell_N_Volume varchar(20) NOT NULL,"
                                    "buy_I_Value varchar(20) NOT NULL,"
                                    "buy_N_Value varchar(20) NOT NULL,"
                                    "sell_I_Value varchar(20) NOT NULL,"
                                    "sell_N_Value varchar(20) NOT NULL,"
                                    "priceChange varchar(20) NOT NULL,"
                                    "priceMin varchar(20) NOT NULL,"
                                    "priceMax varchar(20) NOT NULL,"
                                    "pClosing varchar(20) NOT NULL,"
                                    "zTotTran varchar(20) NOT NULL,"
                                    "qTotTran5J varchar(20) NOT NULL,"
                                    "qTotCap varchar(20) NOT NULL"
                                    ")"
                                    % (name))
                        conn.commit()
                        pass
                    except:
                        log.error_write(i)
                        continue
                    pass
                else:
                    #badan bayad gozine debug ezafe beshe
                    continue
                    pass
                pass
            conn.close()
            return True
        except:
            log.error_write('')
            return None

    def analize_table(index=None, schema: str = None):
        # self is symbol's index
        if index is None:
            index_list = read.index()
            pass
        else:
            index_list = [index]
            pass
        if schema is None:
            schema = 'analize'
            pass
        else:
            pass
        conn = mariadb.connect(
            user="root",
            password="Unique2213",
            host="localhost",
            port=3306,
            database=schema
        )
        for i in index_list:
            if search.table(index=i, schema="analize") is False:
                try:
                    name = "nmd" + str(i)
                    cur = conn.cursor()
                    cur.execute("CREATE TABLE IF NOT EXISTS %s ("
                                "dEven varchar(20) UNIQUE NOT NULL PRIMARY KEY,"
                                "percentage varchar(20) NOT NULL,"
                                "ghodrat_kh_ha varchar(20) NOT NULL,"
                                "ghodrat_fo_ha varchar(20) NOT NULL,"
                                "ghodrat_kh_ho varchar(20) NOT NULL,"
                                "ghodrat_fo_ho varchar(20) NOT NULL,"
                                "ghodrat_khha_khho varchar(20) NOT NULL,"
                                "ghodrat_hjmkhha_hjmkhho varchar(20) NOT NULL,"
                                "ghodrat_foha_foho varchar(20) NOT NULL,"
                                "ghodrat_hjmfoha_hjmfoho varchar(20) NOT NULL"
                                ")"
                                % (name))
                    conn.commit()
                    pass
                except:
                    log.error_write(i)
                    continue
                pass
            else:
                # badan bayad gozine debug ezafe beshe
                continue
                pass
            pass
        conn.close()
        return True
        pass


class LiveTableCreate:
    def price_table(index=None):
        try:
            # self is symbol's index
            if index is None:
                index_list = read.index()
                pass
            else:
                index_list = [index]
                pass
            conn = mariadb.connect(
                user="root",
                password="Unique2213",
                host="localhost",
                port=3306,
                database="live_moneymaker_update"
            )
            for i in index_list:
                if search.table(index=i) is False:
                    try:
                        name = "nmd" + str(i)
                        cur = conn.cursor()
                        cur.execute("CREATE TABLE IF NOT EXISTS %s ("
                                    "finalLastDate varchar(20) NOT NULL,"
                                    "lastHEven varchar(20) UNIQUE NOT NULL PRIMARY KEY,"
                                    "buy_CountI varchar(20) NOT NULL,"
                                    "buy_I_Volume varchar(20) NOT NULL,"
                                    "sell_CountI varchar(20) NOT NULL,"
                                    "sell_I_Volume varchar(20) NOT NULL,"
                                    "buy_CountN varchar(20) NOT NULL,"
                                    "buy_N_Volume varchar(20) NOT NULL,"
                                    "sell_CountN varchar(20) NOT NULL,"
                                    "priceYesterday varchar(20) NOT NULL,"
                                    "priceFirst varchar(20) NOT NULL,"
                                    "sell_I_Value varchar(20) NOT NULL,"
                                    "sell_N_Value varchar(20) NOT NULL,"
                                    "priceChange varchar(20) NOT NULL,"
                                    "priceMin varchar(20) NOT NULL,"
                                    "priceMax varchar(20) NOT NULL,"
                                    "pClosing varchar(20) NOT NULL,"
                                    "pDrCotVal varchar(20) NOT NULL,"
                                    "zTotTran varchar(20) NOT NULL,"
                                    "qTotTran5J varchar(20) NOT NULL,"
                                    "qTotCap varchar(20) NOT NULL"
                                    ")"
                                    % (name))
                        conn.commit()
                        pass
                    except:
                        log.error_write(i)
                    pass
                else:
                    #badan bayad gozine debug ezafe beshe
                    continue
                    pass
                pass
            conn.close()
            return True
        except:
            log.error_write('')
            return False

    def analize_table(index=None):
        try:
            HistoryTableCreate.analize_table(index=index, schema='live_analyze_update')
            return True
        except:
            log.error_write('')
            return False


def temp_table_creator(namad_symbol):
    error_count = 0
    existance = search.table(namad_symbol)
    if existance is True:
        return None
    else:
        pass
    while error_count < 7:
        try:
            con = sql.connect(locator.temp_database(), check_same_thread=False)
            cur = con.cursor()
            con.execute("CREATE TABLE '%s'("
                        "dEven integer (10) UNIQUE PRIMARY KEY,"
                        "buy_I_Count integer (12),"
                        "buy_I_Volume integer (12),"
                        "sell_I_Count integer (12),"
                        "sell_I_Volume integer (12),"
                        "buy_N_Count integer (12),"
                        "buy_N_Volume integer (12),"
                        "sell_N_Count integer (12),"
                        "sell_N_Volume integer (12),"
                        "ghodrat_kh_ha integer (12),"
                        "ghodrat_fo_ha integer (12),"
                        "ghodrat_kh_ho integer (12),"
                        "ghodrat_fo_ho integer (12),"
                        "ghodrat_khha_khho integer (12),"
                        "ghodrat_hjmkhha_hjmkhho integer (12),"
                        "ghodrat_foha_foho integer (12),"
                        "ghodrat_hjmfoha_hjmfoho integer (12),"
                        "percentage integer (12),"
                        "pClosing integer (12),"
                        "zTotTran integer (12),"
                        "qTotTran5J integer (12),"
                        "base_volume integer (12),"
                        "qTotCap integer (12)"
                        ")"
                        % (namad_symbol))
            con.commit()
            con.close()
            return None
            pass
        except:
            error_count += 1
            sleep(random.random())
            if error_count >= 7:
                log.error_write(search.index(namad_symbol))
                return None
            else:
                pass
            pass
        pass
    pass


class log:
    def error_write(index, **kwargs):
        # declaring variables
        exc = ['0', '0', '0', '0', '0']
        trc = ['0', '0', '0', '0', '0']
        code = ""
        error_message = ""
        exc = sys.exc_info()
        _, _, tb = exc
        trc = traceback.extract_tb(tb)[0]
        error_message = re.sub("'", "", str(exc[1]))
        if len(error_message) > 200:
            error_message = error_message[:299]
            pass
        else:
            pass
        code = trc[3]
        code = re.sub("'", "", code)
        dic = [{
            'insCode': index,
            'module': trc[0],
            'function': trc[2],
            'line': int(trc[1]),
            'code': code,
            'error_message': error_message
        }]
        try:
            save_df = pd.DataFrame.from_dict(dic)
            engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306"
                                   "/log_database")
            counter = save_df.to_sql(name='error_log', con=engine,
                                     if_exists='append', index=False)
            pass
        except:
            print(sys.exc_info())
            '''fallback baraye shomardane tedade eun shodane tabe 
            log tavasote log hast'''
            fallback = kwargs.get('fallback', None)
            if fallback is None:
                fallback = 1
                pass
            elif fallback < 3:
                log.error_write(index, fallback=1)
                fallback += 1
                pass
            else:
                return None

    def list(self):
        error_count = 0
        error_message = ""
        while error_count < 6:
            try:
                conn = mariadb.connect(
                    user="root",
                    password="Unique2213",
                    host="localhost",
                    port=3306,
                    database="log"
                )
                cur = conn.cursor()
                result = cur.execute((r"SELECT dEven FROM '%s' ORDER BY date DESC"
                                      % (self)).replace("'", ""))
                result = result.fetchall()
                if result is None:
                    return False
                else:
                    return_list = []
                    for i in result:
                        return_list.append(i[0])
                        pass
                    conn.commit()
                    conn.close()
                    break
                    pass
                pass
            except:
                error_count += 1
                sleep(random.random())
                log.error_write(self)
                pass
            pass
        if error_count > 6:
            log.error_write(self)
            return None
            pass
        else:
            return return_list

    def last_date(self, date):
        conn = mariadb.connect(
            user="root",
            password="Unique2213",
            host="localhost",
            port=3306,
            database="log"
        )
        cur = conn.cursor()
        result = cur.execute((r"SELECT dEven FROM '%s' ORDER BY date DESC"
                              % (self)).replace("'", ""))
        result = result.fetchone()
        conn.commit()
        conn.close()
        del conn
        if result is None:
            return False
        else:
            last_date = result[0]
        if date == last_date or last_date > date:
            return True
        else:
            return False
        pass


class black_list:

    @staticmethod
    def read():
        try:
            conn = mariadb.connect(
                user="root",
                password="Unique2213",
                host="localhost",
                port=3306,
                database="manager"
            )
            cur = conn.cursor()
            cur.execute(r"SELECT insCode FROM tblblacklist")
            conn.commit()
            conn.close()
            del conn
            black_list: list = []
            for i in cur:
                black_list.append(i[0])
                pass
            return black_list
        except:
            log.error_write("")
            return None

    def search(self):
        try:
            # baz kardane sql va khandane tblnamadhatemp
            conn = mariadb.connect(
                user="root",
                password="Unique2213",
                host="localhost",
                port=3306,
                database="manager"
            )
            cur = conn.cursor()
            cur.execute(("SELECT insCode FROM tblblacklist WHERE insCode LIKE %s"
                         % (self)))
            conn.commit()
            conn.close()
            del conn
            if cur.fetchone() is None:
                return False
                pass
            else:
                return True
        except:
            try:
                conn.commit()
                conn.close()
                del conn
                pass
            except:
                pass
            log.error_write(search.index(self))
            return True
        pass

    def write(pd_dataframe: pandas.DataFrame):
        try:
            index = pd_dataframe.loc[0, 'insCode']
            engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306/manager")
            result = pd_dataframe.to_sql(name='tblblacklist', con=engine,
                                         if_exists='append', index=False)
            # killing the engine
            engine.dispose()
            del engine
            # return saved entries
            return result
        except:
            log.error_write(index)
            return None
        pass


def duplicate_remover(namad_entry):
    conn = mariadb.connect(
        user="root",
        password="Unique2213",
        host="localhost",
        port=3306,
        database="moneymaker"
    )
    cur = conn.cursor()
    cur.execute((r"DROP TABLE IF EXISTS '%s'"
                 % (namad_entry)).replace("'", ""))
    conn.commit()
    conn.close()
    return None


def SessionKiller():
    try:
        # baz kardane sql va khandane tblnamadha
        conn = mariadb.connect(
            user="root",
            password="Unique2213",
            host="localhost",
            port=3306,
            database="manager"
        )
        cur = conn.cursor()
        cur.execute(r"kill USER username;")
        conn.commit()
        conn.close()
        del conn
        return True
    except:
        try:
            pass
        except:
            pass
        print(sys.exc_info)
        log.error_write("")
        return False


"""class Regulator:
    @staticmethod
    database_length():"""


class locator():

    @staticmethod
    def database():
        return r'C:\Moneymaker2.0\database\saham.db'

    @staticmethod
    def temp_database():
        return r'C:\Moneymaker2.0\database\temp.db'


# def sqlLocator():

class schemas:
    def __init__(self):
        pass

    @staticmethod
    def history_analyze():
        return "analize"

    @staticmethod
    def history_moneymaker():
        return "moneymaker"

    @staticmethod
    def live_analyze():
        return "live_analyze_update"

    @staticmethod
    def live_moneymaker():
        return "live_moneymaker_update"

    @staticmethod
    def live_best_limits():
        return "best_limits"

    @staticmethod
    def close_best_limits():
        return "close_best_limits"
"""