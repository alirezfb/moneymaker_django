# -*- coding: utf-8 -*-
""""
in module 2 ghesmat dare
ghesmate aval ye object koli shamel nam va parameter ha daryaft mikone
va bad karaye mohasebati va analize ro anjam mide va save mikone va barmigardoone
"""

# Import Section
import sys
import numpy as np
from time import sleep
import pandas as pd
import warnings
import django
import operator

try:
    from . import tse_time
    from . import my_sql
    from . import tse_connect
except:
    import tse_connect
    import tse_time
    import my_sql


# Import Section

# warnings.filterwarnings('ignore')


def list_calculate_pd_2(index, pd_dataframe: pd.DataFrame, live: bool):
    try:
        if pd_dataframe is None:
            return None
        elif len(pd_dataframe.index) < 800:
            loop_length = len(pd_dataframe.index) - 1
        else:
            loop_length = 800
            pd_dataframe.drop(pd_dataframe.index[loop_length - 1:pd_dataframe.shape[0]], axis=0, inplace=True)
            pass
        dic: dict = {
            "percentage": [],
            "ghodrat_kh_ha": [],
            "ghodrat_fo_ha": [],
            "ghodrat_kh_ho": [],
            "ghodrat_fo_ho": [],
            "ghodrat_khha_khho": [],
            "ghodrat_hjmkhha_hjmkhho": [],
            "ghodrat_foha_foho": [],
            "ghodrat_hjmfoha_hjmfoho": []
        }
        # Loope mohasebati list ha
        for i in range(0, loop_length + 1):
            df_series = pd_dataframe.loc[i]
            dic["percentage"].append(calculate_pd.percentage(df_series, pd_dataframe, i))
            dic["ghodrat_kh_ha"].append(calculate_pd.ghodrat_kh_ha(df_series))
            dic["ghodrat_fo_ha"].append(calculate_pd.ghodrat_fo_ha(df_series))
            dic["ghodrat_kh_ho"].append(calculate_pd.ghodrat_kh_ho(df_series))
            dic["ghodrat_fo_ho"].append(calculate_pd.ghodrat_fo_ho(df_series))
            dic["ghodrat_khha_khho"].append(calculate_pd.ghodrat_khha_khho(df_series))
            dic["ghodrat_hjmkhha_hjmkhho"].append(calculate_pd.ghodrat_hjmkhha_hjmkhho(df_series))
            dic["ghodrat_foha_foho"].append(calculate_pd.ghodrat_foha_foho(df_series))
            dic["ghodrat_hjmfoha_hjmfoho"].append(calculate_pd.ghodrat_hjmfoha_hjmfoho(df_series))
            pass
        temp_df = pd.DataFrame.from_dict(dic)
        del dic
        if live is False:
            temp_df.insert(1, 'insCode', pd_dataframe['insCode'])
            temp_df.insert(1, 'dEven', pd_dataframe['dEven'])
            pass
        else:
            pass
        # temp_df['insCode'] = pd_dataframe['insCode'].values
        """pd_dataframe.drop(['pClosing', 'buy_I_Count', 'buy_I_Volume',
                           'sell_I_Count', 'sell_I_Volume', 'buy_N_Count',
                           'buy_N_Volume', 'sell_N_Count', 'sell_N_Volume',
                           'zTotTran', 'qTotTran5J', 'qTotCap', 'priceChange',
                           'priceMin', 'priceMax'], axis=1, inplace=True)
        pd_dataframe = pd.concat([pd_dataframe, temp_df], axis=1)"""
        return temp_df
    except:
        my_sql.log.error_write(index)
        return None


"""this def is for filtering pandas dataframe and deleteing the non matching
    rows and returning the matching ones"""


class filter:

    def operand(index, pd_dataframe, first_operand, second_operand, op):
        try:
            # declaring operator shortcuts
            ops = {">": operator.gt, "==": operator.is_, "<": operator.lt}
            # dataframe length as loop length
            loop_length = len(pd_dataframe.index)
            # loop for filtering
            for i in range(0, loop_length):
                df_series = pd_dataframe.loc[i]
                # automatic filter generator
                if not ops[op](float(df_series[first_operand]), float(df_series[second_operand])):
                    # dropping non matching items
                    pd_dataframe.drop(i, axis=0, inplace=True)
                    pass
                else:
                    pass
                pass
            # resseting dataframe index
            pd_dataframe.reset_index(inplace=True)
            return pd_dataframe
        except:
            my_sql.write(index)

    def before(index, analize_df, moneymaker_df, op: str):
        try:
            # declaring operator shortcuts
            ops = {"positive": operator.gt, "negative": operator.lt}
            # dataframe length as loop length
            loop_length = len(moneymaker_df.index)
            # loop for filtering
            for i in range(0, loop_length):
                df_series = analize_df.loc[i]
                if i == 0:
                    continue
                elif ops[op](float(df_series['percentage']), 0):
                    pass
                else:
                    # dropping non matching items
                    analize_df.drop(i - 1, axis=0, inplace=True)
                    moneymaker_df.drop(i - 1, axis=0, inplace=True)
                    pass
                pass
            # reseting dataframe index
            analize_df.reset_index(inplace=True, drop=True)
            moneymaker_df.reset_index(inplace=True, drop=True)
            return analize_df, moneymaker_df
        except:
            my_sql.log.error_write(index)

    """def before_negative(index, analize_df, moneymaker_df):
        try:
            # dataframe length as loop length
            loop_length = len(moneymaker_df.index)
            # loop for filtering
            for i in range(0,loop_length):
                df_series = analize_df.loc[i]
                if i == 0:
                    continue
                elif float(df_series['percentage']) < 0:
                    pass
                else:
                    # dropping non matching items
                    analize_df.drop(i-1, axis=0, inplace=True)
                    moneymaker_df.drop(i-1, axis=0, inplace=True)
                    pass
                pass
            # resseting dataframe index
            analize_df.reset_index(inplace=True, drop=True)
            moneymaker_df.reset_index(inplace=True, drop=True)
            return analize_df, moneymaker_df  
        except:
            my_sql.log.write(index)"""

    def counter(index, pd_dataframe):
        # counter dic
        dic: dict = {
            "name": my_sql.search.names(index),
            "index": str(index),
            "percentage": 0,
            "ghodrat_kh_ha": 0,
            "ghodrat_fo_ha": 0,
            "ghodrat_kh_ho": 0,
            "ghodrat_fo_ho": 0,
            'ghodrat_kh_ho_ha': 0,
            'ghodrat_kh_ha_ho': 0,
            "ghodrat_khha_khho": 0,
            "ghodrat_hjmkhha_hjmkhho": 0,
            "ghodrat_foha_foho": 0,
            "ghodrat_hjmfoha_hjmfoho": 0
        }
        try:
            # dataframe length as loop length
            loop_length = len(pd_dataframe.index)
            # loop for filtering
            for i in range(0, loop_length):
                df_series = pd_dataframe.loc[i]
                if df_series['ghodrat_kh_ha'] > df_series['ghodrat_fo_ha'] * 2:
                    dic['ghodrat_kh_ha'] += 1
                    pass
                if df_series['ghodrat_fo_ha'] > df_series['ghodrat_kh_ha']:
                    dic['ghodrat_fo_ha'] += 1
                    pass
                if df_series['ghodrat_kh_ho'] > df_series['ghodrat_fo_ho'] * 2:
                    dic['ghodrat_kh_ho'] += 1
                    pass
                if df_series['ghodrat_fo_ho'] > df_series['ghodrat_kh_ho']:
                    dic['ghodrat_fo_ho'] += 1
                    pass
                if df_series['ghodrat_kh_ha'] > df_series['ghodrat_kh_ho'] * 2:
                    dic['ghodrat_khha_khho'] += 1
                    pass
                if df_series['ghodrat_kh_ho'] > df_series['ghodrat_kh_ha']:
                    dic['ghodrat_kh_ho_ha'] += 1
                    pass
                pass
            percent_key = 100 / loop_length
            dic['ghodrat_kh_ha'] = round(dic['ghodrat_kh_ha'] * percent_key, 2)
            dic['ghodrat_fo_ha'] = round(dic['ghodrat_fo_ha'] * percent_key, 2)
            dic['ghodrat_kh_ho'] = round(dic['ghodrat_kh_ho'] * percent_key, 2)
            dic['ghodrat_fo_ho'] = round(dic['ghodrat_fo_ho'] * percent_key, 2)
            dic['ghodrat_khha_khho'] = round(dic['ghodrat_khha_khho'] * percent_key, 2)
            dic['ghodrat_kh_ho_ha'] = round(dic['ghodrat_kh_ho_ha'] * percent_key, 2)
            # resseting dataframe index
            return dic
        except:
            my_sql.log.error_write(index)
            return dic


class calculate_pd:
    def ghodrat_kh_ha(pd):
        try:
            v1 = pd['buy_I_Volume']
            v2 = pd['buy_I_Count']
            if v1 == 0 or v2 == 0:
                result = 0
                pass
            else:
                result = v1 / v2
                result = round(result, 2)
                if np.isnan(result) is True:
                    result = 0
                    pass
                else:
                    pass
                pass
            return result
        except:
            return 0

    def ghodrat_fo_ha(pd):
        try:
            v1 = pd['sell_I_Volume']
            v2 = pd['sell_I_Count']
            if v1 == 0 or v2 == 0:
                result = 0
                pass
            else:
                result = v1 / v2
                result = round(result, 2)
                if np.isnan(result) is True:
                    result = 0
                    pass
                else:
                    pass
                pass
            return result
        except:
            return 0

    def ghodrat_kh_ho(pd):
        try:
            v1 = pd['buy_N_Volume']
            v2 = pd['buy_N_Count']
            if v1 == 0 or v2 == 0:
                result = 0
                pass
            else:
                result = v1 / v2
                result = round(result, 2)
                if np.isnan(result) is True:
                    result = 0
                    pass
                else:
                    pass
                pass
            return result
        except:
            return 0

    def ghodrat_fo_ho(pd):
        try:
            v1 = pd['sell_N_Volume']
            v2 = pd['sell_N_Count']
            if v1 == 0 or v2 == 0:
                result = 0
                pass
            else:
                result = v1 / v2
                result = round(result, 2)
                if np.isnan(result) is True:
                    result = 0
                    pass
                else:
                    pass
                pass
            return result
        except:
            return 0

    def ghodrat_khha_khho(pd):
        try:
            v1 = pd['buy_I_Count']
            v2 = pd['buy_N_Count']
            if v1 == 0 or v2 == 0:
                result = 0
                pass
            else:
                result = v1 / v2
                result = round(result, 2)
                if np.isnan(result) is True:
                    result = 0
                    pass
                else:
                    pass
                pass
            return result
        except:
            return 0

    def ghodrat_hjmkhha_hjmkhho(pd):
        try:
            v1 = pd['buy_I_Volume']
            v2 = pd['buy_N_Volume']
            if v1 == 0 or v2 == 0:
                result = 0
                pass
            else:
                result = v1 / v2
                result = round(result, 2)
                if np.isnan(result) is True:
                    result = 0
                    pass
                else:
                    pass
                pass
            return result
        except:
            return 0

    def ghodrat_foha_foho(pd):
        try:
            v1 = pd['sell_I_Count']
            v2 = pd['sell_N_Count']
            if v1 == 0 or v2 == 0:
                result = 0
                pass
            else:
                result = v1 / v2
                result = round(result, 2)
                if np.isnan(result) is True:
                    result = 0
                    pass
                else:
                    pass
                pass
            return result
        except:
            return 0

    def ghodrat_hjmfoha_hjmfoho(pd):
        try:
            v1 = pd['sell_I_Volume']
            v2 = pd['sell_N_Volume']
            if v1 == 0 or v2 == 0:
                result = 0
                pass
            else:
                result = v1 / v2
                result = round(result, 2)
                if np.isnan(result) is True:
                    result = 0
                    pass
                else:
                    pass
                pass
            return result
        except:
            return 0
        pass

    def percentage(pd, dataframe, count):
        try:
            result = (pd.loc['pClosing'] * 100 / dataframe.loc[count + 1, 'pClosing']) - 100
            result = round(result, 2)
            if np.isnan(result) is True:
                result = 0
                pass
            else:
                pass
            return result
        except:
            return 0
        pass


def dataframe_return(index_list, definition: str = "last_5_best_limit"):
    try:
        result_list = []
        for index in index_list:
            obj = scripts(index=index, only_status=False, df_return=True)
            func = "scripts." + definition + "()"
            temp_res = getattr(obj, definition)()
            if temp_res is None:
                continue
            elif len(temp_res.index) > 0:
                res = (pd.DataFrame(temp_res.sum())).T
                res['index'] = str(index)
                res['name'] = my_sql.search.names(index)
                result_list.append(res)
                pass
            else:
                continue
            pass
        return_df = result_list[0]
        del result_list[0]
        for df in result_list:
            return_df = pd.concat([return_df, df], axis=0, ignore_index=True)
        return_df.columns = ["Hajm Kharid", "Tedad Kharid",
                             "Gheymat Kharid", "Gheymat Foroosh",
                             "Tedad Foroosh", "Hajm Foroosh",
                             "Index", "Name"]
        return return_df
    except:
        my_sql.log.error_write("")
        return None


def sum_best_limit(object_list: list):
    try:
        return_list = []
        # number of lists
        for i in range(0, len(object_list) - 1):
            temp_num = 0
            # number of list objects
            for j in range(0, len(object_list[0]) - 1):
                temp_num += object_list[i][j]
                pass
            return_list.append(temp_num)
            pass
        return return_list
    except:
        my_sql.log.error_write("")
        return None


def django_temp(live=True):
    try:
        if live is True:
            script = "select * from live_best_limits"
        else:
            script = "select * from all_best_limits"
        res = my_sql.search.script("best_limits", script, df_return=True)
        return res
    except:
        my_sql.log.error_write("")
        return None


def list_return(index_list, definition):
    try:
        result_list = []
        for index in index_list:
            obj = scripts(index=index, only_status=True, df_return=False)
            func = "scripts." + definition + "()"
            res = getattr(obj, definition)()
            if res is True:
                result_list.append(index)
            else:
                pass
        return result_list
    except:
        my_sql.log.error_write("")
        return None


def close_market_list(index_list):
    try:
        result_list = []
        definition = "last_5_best_limit"
        for index in index_list:
            obj = scripts(index=index, only_status=False, df_return=True)
            func = "scripts." + definition + "()"
            res = getattr(obj, definition)()
        return result_list
    except:
        my_sql.log.error_write("")
        return None


def list_compare(index_list, *args):
    list_of_lists = []
    for definition in args:
        list_of_lists.append(list_return(index_list, definition))
    return_list = list_of_lists[0]
    for i in range(1, len(list_of_lists) - 1):
        return_list = [num for num in return_list
                       if num in list_of_lists[i]]
    return return_list


class scripts:
    def __init__(self, index=0, only_status=False, index_list=None, df_return=True, group=True):
        self.name = "nmd" + str(index)
        self.index = index
        self.client_objects = ("buy_I_Volume, buy_N_Volume, buy_CountI, "
                               "buy_CountN, sell_I_Volume, sell_N_Volume, "
                               "sell_CountI, sell_CountN")
        self.closing_objects = ""
        self.day = tse_time.today_str(history=False)
        self.time = tse_time.current_time_str()[:3]
        self.schema = my_sql.schemas()
        self.only_status = only_status
        self.index_list = index_list
        self.df_return = df_return
        self.market_state = tse_connect.market_state()
        self.today_str = tse_time.today_str()
        self.time = tse_time.latest_ten_minutes()

    class columns:
        def __init__(self):
            self.best_limits_objects = ["qTitMeDem", "zOrdMeDem", "pMeDem",
                                        "pMeOf", "zOrdMeOf", "qTitMeOf"]
            self.space = " "
            pass

        def best_limits(self, sum_group=False):
            return_object = ""
            if sum_group is True:
                for obj in self.best_limits_objects:
                    return_object += self.space + "SUM(" + obj + ") " + obj + ","
            else:
                for obj in self.best_limits_objects:
                    return_object += self.space + obj + ","
            return return_object[:-1]

    class objects:
        def __init__(self):
            self.select = "SELECT"
            self.space_char = " "
            self.all_word = "*"
            self.from_word = "FROM"
            self.where_word = "WHERE"
            self.and_word = "AND"
            self.order_by_word = "ORDER BY"
            self.limit_word = "LIMIT"

        def select_script(self, select_all=True, sum_group=False):
            columns = scripts.columns()
            if select_all is True:
                return self.select + self.space_char + self.all_word
            elif sum_group is True:
                return (self.select +
                        columns.best_limits(sum_group))
            else:
                return self.select + columns.best_limits()

        def from_script(self, index=0, name=""):
            if index != 0:
                return (self.space_char + self.from_word +
                        self.space_char + "nmd" + str(index))
            else:
                return self.space_char + self.from_word + self.space_char + name

        def where_script(self, *args):
            if len(args) == 0:
                return ""
            else:
                return_obj = self.space_char + self.where_word
                for condition in args:
                    return_obj += self.space_char + condition + self.space_char + self.and_word
                return return_obj[:-4]

        def order_by_script(self, condition=""):
            return_obj = self.space_char + self.order_by_word
            if condition == "":
                return ""
            else:
                return return_obj + self.space_char + condition

        def limit_script(self, condition=100):
            return (self.space_char + self.limit_word +
                    self.space_char + str(condition))




    def __return_process(self, schema, script):
        try:
            return_object = my_sql.search.script(schema=schema, script=script, df_return=self.df_return)
            if self.only_status is True:
                kk = scripts.objects  # when dataframe
                if self.df_return is True:
                    if len(return_object.index) > 0:
                        return True
                    else:
                        return False
                # when list
                elif len(return_object) > 0:
                    return True
                else:
                    return False
            else:
                return return_object
        except:
            my_sql.log.error_write(self.index)
            return None

    def latest_ghodrat_kh_ha(self):
        try:
            # client objects live
            script = ("select * from " + self.name +
                      (" where buy_CountI < sell_CountI and"
                       " buy_I_Volume/buy_CountI > sell_I_Volume/sell_CountI"
                       " and finalLastDate LIKE " + self.day +
                       " and lastHEven LIKE " + "'" + self.time.latest_ten_minutes() +
                       " ORDER BY lastHEven DESC Limit 1"))
            return scripts.__return_process(self, self.schema.live_moneymaker(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None

    def latest_best_limit(self):
        try:
            script = ("select " + self.best_limits_objects + " from " +
                      self.name + (" where datetime between NOW() -" +
                                   " INTERVAL 3 MINUTE AND NOW() Limit 1"))
            return scripts.__return_process(self, self.schema.best_limits(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None

    def sum_live_best_limit(self):
        try:
            script = ("select " + self.best_limits_objects + " from " +
                      self.name + (" where datetime between NOW() -" +
                                   " INTERVAL 3 MINUTE AND NOW() Limit 1"))
            return scripts.__return_process(self, self.schema.best_limits(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None

    def read_sum_live_best_limit(self):
        try:
            script = ("select * from live_best_limits" +
                      (" where 'Hajm Kharid' >" +
                       " 'Hajm Foroosh'"))
            return scripts.__return_process(self, self.schema.best_limits(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None

    """def latest_best_limit(self):
        try:
            script = ("select " + self.best_limits_objects + " from " +
                      self.name + (" where datetime between NOW() -" +
                                   " INTERVAL 3 MINUTE AND NOW() Limit 1"))
            dataframe = scripts.__return_process(self, self.schema.best_limits(), script=script)
            return scripts.__operations(self, "qTitMeDem/zOrdMeDem", "(qTitMeOf/zOrdMeOf)*2")
        except:
            my_sql.log.error_write(self.index)
            return None"""

    def all_live_best_limits(self):
        try:
            script = ("select " + self.best_limits_objects + " from " +
                      self.name + " Limit 1")
            return scripts.__return_process(self, self.schema.best_limits(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None

    def latest_ha_be_ho(self):
        try:
            script = (" select * from " + self.name +
                      " where buy_I_Volume > ((sell_I_Volume)*2)"
                      " and buy_I_Volume > buy_N_Volume and"
                      " finalLastDate = " + self.today_str +
                      " and lastHEven < " + self.time +
                      " ORDER BY lastHEven DESC Limit 1")
            return scripts.__return_process(self, self.schema.live_moneymaker(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None

    def last_5_best_limit(self):
        try:
            script = ("select SUM(qTitMeDem), SUM(zOrdMeDem),"
                      " SUM(pMeDem), SUM(pMeOf), SUM(zOrdMeOf),"
                      " SUM(qTitMeOf) from nmd46348559193224090" +
                      " where datetime between NOW() -" +
                      " INTERVAL 3 HOUR AND NOW()")
            return scripts.__return_process(self, self.schema.best_limits(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None

    def all_close_best_limit(self):
        try:
            script = ("select " + self.best_limits_objects +
                      " from " + self.name +
                      " LIMIT 5")
            return scripts.__return_process(self, self.schema.close_best_limits(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None

    def close_best_limit(self):
        try:
            script = ("select " + self.best_limits_objects +
                      " from " + self.name +
                      " where zOrdMeDem >" +
                      " ((zOrdMeOf)*3) and" +
                      " qTitMeDem/zOrdMeDem >" +
                      " (qTitMeOf/zOrdMeOf)*2" +
                      " LIMIT 5")
            return scripts.__return_process(self, self.schema.close_best_limits(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None

    def close_ghodrat_kh_ha(self):
        try:
            script = ("select * from " +
                      self.name + " where ghodrat_kh_ha >" +
                      " ghodrat_fo_ha * 3 and" +
                      " ghodrat_kh_ha > ghodrat_kh_ho" +
                      " and dEven Like " + str(self.market_state.last_open()))
            return scripts.__return_process(self, self.schema.history_analyze(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None

    def close_ha_be_ho(self):
        try:
            script = ("select * from " +
                      self.name + (" where buy_I_Volume >" +
                                   " sell_N_Volume and"
                                   " dEven IS LIKE " + self.today_str +
                                   " ORDER BY dEven DESC LIMIT 1"))
            return scripts.__return_process(self, self.schema.live_moneymaker(), script=script)
        except:
            my_sql.log.error_write(self.index)
            return None


a = scripts.objects()
b = (a.select_script() + a.from_script(name="nmd4634") +
     a.where_script("mamad > 4", 'j<v', " kir>kos") +
     a.order_by_script("ffff") + a.limit_script(3))
print(b)
