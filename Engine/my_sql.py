# -*- coding: utf-8 -*-
"""MARIADB COMMANDS
    SHOW STATUS WHERE `variable_name` = 'Threads_connected';
    kill USER username;
"""

from sqlalchemy import create_engine
from time import sleep
import mariadb
import pandas
import re
import traceback
import sys
import random
import pandas as pd
import tse_time


# START

class ObjProperties:
    def __init__(self):
        pass

    class Crypto:
        def __init__(self):
            pass

        obj_type = 'crypto'

        class ChartData:
            fa_charset = False
            date_field = 'open_time'
            schema = 'crypto_chart_data'
            obj_type = 'crypto'
            table_create_columns = ("open_time datetime PRIMARY KEY UNIQUE null,"
                                    "open double null,"
                                    "high double null,"
                                    "low double null,"
                                    "close double null,"
                                    "first_sym_vol double null,"
                                    "close_time bigint null,"
                                    "second_sym_vol double null,"
                                    "u0 bigint null,"
                                    "u1 text null,"
                                    "u2 text null,"
                                    "u3 text null")

    class Tse:
        def __init__(self):
            self.obj_type = 'tse'
            pass

        obj_type = 'tse'

        class Manager:
            def __str__(self):
                pass

            class MarketStatus:
                fa_charset = False
                date_field = 'todayDEven'
                obj_type = 'tse'
                schema = 'manager'
                table_create_columns = ("todayDEven INT UNIQUE NOT NULL PRIMARY KEY,"
                                        "marketActivityDEven INT NULL")

        class MoneymakerHistory:
            fa_charset = False
            date_field = 'dEven'
            obj_type = 'tse'
            schema = 'moneymaker'
            table_create_columns = ("dEven varchar(20) UNIQUE NOT NULL PRIMARY KEY,"
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
                                    "qTotCap varchar(20) NOT NULL")

        class MoneymakerLive:
            fa_charset = False
            date_field = 'finalLastDate'
            time_field = 'lastHEven'
            obj_type = 'tse'
            schema = 'live_moneymaker_update'
            table_create_columns = ("finalLastDate varchar(20) NOT NULL,"
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
                                    "qTotCap varchar(20) NOT NULL")

        class AnalyzeHistory:
            fa_charset = False
            date_field = 'dEven'
            obj_type = 'tse'
            schema = 'analize'
            table_create_columns = "dEven varchar(20) UNIQUE NOT NULL PRIMARY KEY," \
                                   "percentage varchar(20) NOT NULL," \
                                   "ghodrat_kh_ha varchar(20) NOT NULL," \
                                   "ghodrat_fo_ha varchar(20) NOT NULL," \
                                   "ghodrat_kh_ho varchar(20) NOT NULL," \
                                   "ghodrat_fo_ho varchar(20) NOT NULL," \
                                   "ghodrat_khha_khho varchar(20) NOT NULL," \
                                   "ghodrat_hjmkhha_hjmkhho varchar(20) NOT NULL," \
                                   "ghodrat_foha_foho varchar(20) NOT NULL," \
                                   "ghodrat_hjmfoha_hjmfoho varchar(20) NOT NULL"

        class AnalyzeLive:
            fa_charset = False
            date_field = 'finalLastDate'
            time_field = 'lastHEven'
            obj_type = 'tse'
            schema = 'live_analyze_update'

        class BestLimitsLive:
            fa_charset = False
            date_field = 'datetime'
            obj_type = 'tse'
            schema = 'best_limits'
            table_create_columns = ("datetime  timestamp default current_timestamp() null,"
                                    "number mediumint null,"
                                    "qTitMeDem int null,"
                                    "zOrdMeDem mediumint null,"
                                    "pMeDem mediumint null,"
                                    "pMeOf mediumint null,"
                                    "zOrdMeOf mediumint null,"
                                    "qTitMeOf int null")

        class BestLimitsHistory:
            fa_charset = False
            date_field = ''
            obj_type = 'tse'
            schema = 'close_best_limits'
            table_create_columns = ("number bigint null,"
                                    "qTitMeDem bigint null,"
                                    "zOrdMeDem bigint null,"
                                    "pMeDem double null,"
                                    "pMeOf double null,"
                                    "zOrdMeOf bigint null,"
                                    "qTitMeOf bigint null")

        class SumCloseBestLimits:
            fa_charset = False
            date_field = ''
            obj_type = 'tse'
            schema = 'sum_close_best_limits'
            table_create_columns = ("qTitMeDem int null,"
                                    "zOrdMeDem mediumint null,"
                                    "pMeDem mediumint null,"
                                    "pMeOf mediumint null,"
                                    "zOrdMeOf mediumint null,"
                                    "qTitMeOf int null")

        class SumLiveBestLimits:
            fa_charset = False
            date_field = ''
            obj_type = 'tse'
            schema = 'sum_live_best_limits'
            table_create_columns = ("qTitMeDem int null,"
                                    "zOrdMeDem mediumint null,"
                                    "pMeDem mediumint null,"
                                    "pMeOf mediumint null,"
                                    "zOrdMeOf mediumint null,"
                                    "qTitMeOf int null")

        class BulkSomeCloseBestLimits:
            def __init__(self):
                self.obj_type = ObjProperties.Tse.obj_type

            fa_charset = True
            date_field = ''
            obj_type = 'tse'
            schema = 'sum_close_best_limits'
            table_create_columns = ("name varchar(20) null,"
                                    "qTitMeDem int null,"
                                    "zOrdMeDem mediumint null,"
                                    "pMeDem mediumint null,"
                                    "pMeOf mediumint null,"
                                    "zOrdMeOf mediumint null,"
                                    "qTitMeOf int null")

        class TblLog:
            def __init__(self):
                pass

            obj_type = "manager"

        class TblNamadha:
            def __init__(self):
                pass

            schema = "manager"

        class TblBlacklist:
            def __init__(self):
                pass

            schema = "manager"


def write_table(dataframe, tbl_name, obj, existing_dates=None, truncate=False, save_limit=10000):
    for i in range(0, 2):
        try:
            if dataframe is None:
                return 0
            else:
                pass
            # making a copy to protect form changes
            clone_dataframe = dataframe.copy(deep=False)

            # extract schema and datefield name from object
            schema = obj.schema
            date_field = obj.date_field
            # checking if the table exists and create it if not
            create_table(obj, tbl_name)
            # truncate table if needed
            if truncate is True:
                truncate_table(schema, tbl_name)
                last_saved_date = 0
            # getting last saved dates if truncate isn't used
            elif existing_dates is None:
                existing_dates = search_dates(tbl_name, obj, list_return=True)
                last_saved_date = int(existing_dates[0])
            # declare last_saved_date for when we have existing date and don't truncate
            else:
                last_saved_date = int(existing_dates[0])
                pass
            '''error check is for the first loop with existing dates has failed
            and static save is needed'''
            error_check = False
            # connecting to database
            engine = create_engine("mariadb+mariadbconnector://" +
                                   "root:Unique2213@127.0.0.1:3306/" +
                                   schema)
            # adding to database
            if error_check is False and last_saved_date != 0:
                # declaring variables
                loop_counter = 0
                ''' this loop is for when we have existing date list
                                    and we check for existing records in db '''
                # finding columns that needs to be saved
                for date in clone_dataframe[date_field]:
                    if last_saved_date >= int(date):
                        break
                    elif loop_counter > save_limit:
                        break
                    else:
                        loop_counter += 1
                # save to database
                if loop_counter == 0:
                    ''' when there isn't any new records in dataframe'''
                    row_save_count = 0
                else:
                    ''' for when there are some records in db and 
                                            to sql function saves only columns that
                                            are not saved '''
                    clone_dataframe.drop(clone_dataframe.index[loop_counter:], axis=0, inplace=True)
                    row_save_count = clone_dataframe.to_sql(name=tbl_name, con=engine,
                                                            if_exists='append', index=False)
            elif search_table(tbl_name, obj) is True:
                ''' when table exists and either we don't have existing 
                    date list and have to go static and save one by one record
                    or there was some error saving dynamically '''
                row_save_count = clone_dataframe.to_sql(name=tbl_name, con=engine,
                                                        if_exists='append', index=False,
                                                        chunksize=1)
            else:
                ''' when there is no existing table and there is no 
                    existing date list have to create table and save
                    records all at once '''
                row_save_count = clone_dataframe.to_sql(name=tbl_name, con=engine,
                                                        if_exists='append', index=False)
            # killing the engine
            engine.dispose()
            del engine
            # return saved entries
            return row_save_count
        except:
            try:
                Log.error_write(tbl_name)
                error_check = True
                if i == 0:
                    # when there is a null or nan record in dataframe
                    clone_dataframe = dataframe.copy(deep=False)
                    clone_dataframe.fillna(0)
                else:
                    engine.dispose()
                    del engine
            except:
                pass
            return 0


def read_table(tbl_name, obj, column_name=None, list_return=True):
    try:
        # baz kardane sql va khandane tblnamadhatemp
        db_object = DbConnect(obj.schema)
        if column_name is not None:
            cur = db_object.select(r"SELECT %s FROM %s "
                                   % (column_name, tbl_name))
        else:
            cur = db_object.select(r"SELECT * FROM %s "
                                   % tbl_name)
            pass
        if list_return is True:
            return_object = cur.fetchall()
            if len(return_object) < 1:
                return None
            else:
                return list(return_object[0])
        else:
            return_object = cur.fetchone()
            if return_object is None:
                return None
            else:
                return return_object[0]
    except:
        Log.error_write("")


def truncate_table(schema, tbl_name):
    try:
        if search_table(tbl_name, schema=schema) is False:
            return None
        else:
            script = "truncate table " + tbl_name
            # baz kardane sql va khandane tblnamadhatemp
            db_object = DbConnect(schema)
            db_object.execute(script)
            return True
    except:
        Log.error_write(Search.index(''))
        return False


def search_dates(tbl_name, obj, list_return=True):
    try:
        date_field = obj.date_field
        schema = obj.schema
        if date_field == '':
            return [0]
        else:
            pass
        # baz kardane sql va khandane tblnamadhatemp
        db_object = DbConnect(schema)
        cur = db_object.select("SELECT %s FROM %s ORDER BY %s DESC"
                               % (date_field, tbl_name, date_field))
        if list_return is True:
            temp_list = cur.fetchall()
            with [] as return_list:
                for i in range(0, len(temp_list)):
                    if tse_time.datetime_type_check(temp_list[i][0]) is True:
                        return_list.append(tse_time.int_db_form(temp_list[i][0]))
                    else:
                        return_list.append(int(temp_list[i][0]))
                if len(return_list) < 1:
                    return [0]
                else:
                    return return_list
        else:
            temp_list = cur.fetchone()
            if temp_list is None:
                return [0]
            else:
                return temp_list[0]
    except:
        Log.error_write("")
        return [0]


class Read:
    def __init__(self):
        pass

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
                db_object = DbConnect("manager")
                cur = db_object.select(r"SELECT name FROM tblnamadha")
                # loop baraye estekhraj kardane esme namadha
                namadha = []
                for i in cur:
                    namadha.append(i[0])
                    pass
                return namadha
            except:
                error_count += 1
                Log.error_write("")
                pass
            pass
        # return if error occured
        return None

    @staticmethod
    def index(bl_check=False):
        try:
            # baz kardane sql va khandane tblnamadhatemp
            script = "SELECT namad_index FROM tblnamadha"
            schema = ObjProperties.Tse.TblNamadha.schema
            db_object = DbConnect(schema)
            cur = db_object.select(script)
            if bl_check is True:
                blacklist = BlackList.read()
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
            Log.error_write("")

    """def analize_list(self):"""

    @staticmethod
    def all_tables(index, schema):
        try:
            # generating table name
            namad_symbol = "nmd" + str(index)
            script = 'SELECT * FROM ' + namad_symbol + ' LIMIT 100'
            # creating database connection string
            connection_string = "mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306/" + schema
            # connecting to database
            engine = create_engine(connection_string)
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
            Log.error_write(index)
            return None


class Search:
    def __init__(self):
        pass

    @staticmethod
    def script(schema: str, script: str, df_return=True, tbl_name=None):
        try:
            if tbl_name is not None:
                if search_table(tbl_name, schema=schema) is False:
                    return None
                else:
                    pass
            else:
                pass
            if df_return is True:
                engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306"
                                       "/" + schema)
                return_object = pd.read_sql(script, engine)
                engine.dispose()
                del engine
                pass
            else:
                # baz kardane sql va khandane tblnamadhatemp
                db_object = DbConnect(schema)
                cur = db_object.select(script)
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
                    pass
                pass
            except:
                pass
            Log.error_write(Search.index(''))
            return None
        pass

    @staticmethod
    def any_table_records(namad_index, table_name, selected_index, schema, searched_item=None, searched_index=None):
        try:
            # baz kardane sql va khandane tblnamadhatemp
            db_object = DbConnect(schema)
            if searched_index or searched_item is None:
                script = ("SELECT %s FROM %s"
                          % (selected_index, table_name))
            else:
                script = ("SELECT %s FROM %s WHERE %s LIKE %s"
                          % (selected_index, table_name,
                             searched_index, searched_item))
            cur = db_object.select(script)
            temp = cur.fetchall()
            with [] as result:
                for i in temp:
                    result.append(i[0])
                    pass
            return result
        except:
            Log.error_write(Search.index(namad_index))
            return None

    @staticmethod
    def names(namad_tbl_name):
        try:
            # baz kardane sql va khandane tblnamadhatemp
            schema = ObjProperties.Tse.TblNamadha.schema
            db_object = DbConnect(schema)
            script = ("SELECT name FROM tblnamadha WHERE namad_index LIKE %s"
                      % (namad_tbl_name))
            cur = db_object.select(script)
            result = cur.fetchone()[0]
            return result
        except:
            Log.error_write(Search.index(namad_tbl_name))
            return None

    @staticmethod
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
            db_object = DbConnect(schema)
            script = ("SHOW TABLES FROM %s LIKE '%s'"
                      % (schema,
                         table_name))
            cur = db_object.select(script)
            if cur.fetchone() is None:
                return False
            else:
                return True
        except:
            Log.error_write(Search.index(table_name))
            return None

    @staticmethod
    def index(namad_tbl_name):
        try:
            # baz kardane sql va khandane tblnamadhatemp
            schema = ObjProperties.Tse.TblNamadha.schema
            db_object = DbConnect(schema)
            script = (r"SELECT namad_index FROM tblnamadha WHERE name LIKE '%s'"
                      % namad_tbl_name)
            cur = db_object.select(script)
            result = cur.fetchone()[0]
            return result
        except:
            Log.error_write(namad_tbl_name)
            return None
        pass

    @staticmethod
    def dates(index, tbl_name=None, schema: str = None):
        if Search.table(index=index) is not True:
            return [0]
        elif schema is None:
            schema = "moneymaker"
            pass
        else:
            pass
        try:
            # baz kardane sql va khandane tblnamadhatemp
            db_object = DbConnect(schema)
            script = (r"SELECT dEven FROM  %s "
                      % tbl_name)
            cur = db_object.select(script)
            q_result = cur.fetchall()
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
            Log.error_write(Search.names(index))
            return [0]
        pass


"""
in tabe baraye khandane nam haye namadha az table namad 
va sakhtane tabali jodagane baraye harkodoom az namad ha
tarahi shode"""


def create_table(obj, tbl_name=None, full_index=False, tse=True):
    try:
        index_list = []
        # when we want to create a full database for tse
        if full_index is True:
            if tse is True:
                index_list = Read.index()
            else:
                #index_list = read.symbols()
                pass
        else:
            index_list = [tbl_name]
        # engine
        db_object = DbConnect(obj.schema)
        for i in index_list:
            if search_table(tbl_name, obj) is False:
                try:
                    script = ("CREATE TABLE IF NOT EXISTS %s ( \n" % i +
                              obj.table_create_columns + "\n )")
                    if obj.fa_charset is True:
                        script += "\ncharset = utf8mb4;"
                    else:
                        pass
                    cur = db_object.select(script)
                except:
                    Log.error_write(i)
                    continue
            else:
                #badan bayad gozine debug ezafe beshe
                continue
        return True
    except:
        Log.error_write('')
        return None


class HistoryTableCreate:
    def __init__(self):
        pass

    @staticmethod
    def price_table(namad_index=None):
        try:
            # self is symbol's index
            if namad_index is None:
                index_list = Read.index()
                pass
            else:
                index_list = [namad_index]
            schema = ObjProperties.Tse.MoneymakerHistory.schema
            db_object = DbConnect(schema)
            for i in index_list:
                if Search.table(index=i) is False:
                    try:
                        name = "nmd" + str(i)
                        script = ("CREATE TABLE IF NOT EXISTS %s ("
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
                                  % name)
                        script_result = db_object.execute(script)
                        pass
                    except:
                        Log.error_write(i)
                        continue
                    pass
                else:
                    #badan bayad gozine debug ezafe beshe
                    continue
                    pass
                pass
            return True
        except:
            Log.error_write('')
            return None

    @staticmethod
    def analyze_table(index=None, schema: str = None):
        # self is symbol's index
        if index is None:
            index_list = Read.index()
            pass
        else:
            index_list = [index]
            pass
        if schema is None:
            schema = 'analize'
            pass
        else:
            pass
        db_object = DbConnect(schema)
        for i in index_list:
            if Search.table(index=i, schema="analize") is False:
                try:
                    name = "nmd" + str(i)
                    script = ("CREATE TABLE IF NOT EXISTS %s ("
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
                              % name)
                    db_object.execute(script)
                except:
                    Log.error_write(i)
                    continue
            else:
                # badan bayad gozine debug ezafe beshe
                continue
        return True


class LiveTableCreate:
    def __init__(self):
        pass

    @staticmethod
    def price_table(index=None):
        try:
            # self is symbol's index
            if index is None:
                index_list = Read.index()
                pass
            else:
                index_list = [index]
                pass
            db_object = DbConnect(ObjProperties.Tse.MoneymakerLive.schema)
            for i in index_list:
                if Search.table(index=i) is False:
                    try:
                        name = "nmd" + str(i)
                        script = ("CREATE TABLE IF NOT EXISTS %s ("
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
                                  % name)
                        db_object.execute(script)
                    except:
                        Log.error_write(i)
                else:
                    #badan bayad gozine debug ezafe beshe
                    continue
            return True
        except:
            Log.error_write('')
            return False

    def analize_table(index=None):
        try:
            HistoryTableCreate.analyze_table(index=index, schema='live_analyze_update')
            return True
        except:
            Log.error_write('')
            return False


class Log:
    def __init__(self):
        pass

    @staticmethod
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
            'symbol': index,
            'module': trc[0],
            'function': trc[2],
            'line': int(trc[1]),
            'code': code,
            'error_message': error_message
        }]
        try:
            save_df = pd.DataFrame.from_dict(dic)
            engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306"
                                   "/manager")
            counter = save_df.to_sql(name='tbllog', con=engine,
                                     if_exists='append', index=False)
            pass
        except:
            '''fallback baraye shomardane tedade eun shodane tabe 
            log tavasote log hast'''
            fallback = kwargs.get('fallback', None)
            if fallback is None:
                fallback = 1
                pass
            elif fallback < 3:
                Log.error_write(index, fallback=1)
                fallback += 1
                pass
            else:
                return None

    @staticmethod
    def list(index):
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
                                      % index).replace("'", ""))
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
                Log.error_write(index)
                pass
            pass
        if error_count > 6:
            Log.error_write(index)
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


def search_table(tbl_name, obj=None, schema=None):
    if obj is not None:
        schema = obj.schema
    else:
        pass
    try:
        # baz kardane sql va khandane tblnamadhatemp
        db_object = DbConnect(schema)
        script = ("SHOW TABLES FROM %s LIKE '%s'"
                  % (schema,
                     tbl_name))
        cur = db_object.select(script)
        if cur.fetchone() is None:
            return False
        else:
            return True
    except:
        Log.error_write(Search.index(tbl_name))
        return None


class BlackList:
    def __init__(self):
        pass

    @staticmethod
    def read():
        try:
            db_object = DbConnect(database="manager")
            cur = db_object.select("SELECT insCode FROM tblblacklist")
            black_list: list = []
            for i in cur:
                black_list.append(i[0])
                pass
            return black_list
        except:
            Log.error_write("")
            return []

    @staticmethod
    def search(namad_index):
        try:
            # baz kardane sql va khandane tblnamadhatemp
            schema = ObjProperties.Tse.TblBlacklist.schema
            db_object = DbConnect(schema)
            script = ("SELECT insCode FROM tblblacklist WHERE insCode LIKE %s"
                      % namad_index)
            cur = db_object.select(script)
            if cur.fetchone() is None:
                return False
                pass
            else:
                return True
        except:
            Log.error_write(Search.index(namad_index))
            return True
        pass

    @staticmethod
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
            Log.error_write(index)
            return None
        pass


class DbConnect:
    def __init__(self,
                 database,
                 user="root",
                 password="Unique2213",
                 host="localhost",
                 port=3306,
                 ):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        pass

    def select(self, script):
        try:
            conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            cur = conn.cursor()
            cur.execute(script)
            conn.commit()
            conn.close()
            return cur
        except:
            try:
                conn.commit()
                conn.close()
                del conn
                pass
            except:
                pass
            new = str(sys.exc_info()[1])
            if "doesn't exist" in new:
                pass
            else:
                pass
            Log.error_write('')
            return []

    def execute(self, script):
        try:
            conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            cur = conn.cursor()
            cur.execute(script)
            conn.commit()
            conn.close()
            return True
        except:
            try:
                conn.commit()
                conn.close()
                del conn
                pass
            except:
                pass
            new = str(sys.exc_info()[1])
            if "doesn't exist" in new:
                pass
            else:
                pass
            Log.error_write('')
            return False


def session_killer():
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
        Log.error_write("")
        return False


"""class Regulator:
    @staticmethod
    database_length():"""


class Locator:

    @staticmethod
    def database():
        return r'C:\Moneymaker2.0\database\saham.db'

    @staticmethod
    def temp_database():
        return r'C:\Moneymaker2.0\database\temp.db'


class Schemas:
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
