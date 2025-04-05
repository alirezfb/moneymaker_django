# -*- coding: utf-8 -*-
""""
in module 2 ghesmat dare
ghesmate aval ye object koli shamel nam va parameter ha daryaft mikone
va bad karaye mohasebati va analize ro anjam mide va save mikone va barmigardoone
"""

# Import Section
import sys
import tse_time
import my_sql
import numpy as np
from time import sleep
import pandas as pd
import warnings
import django
import operator


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
        print(sys.exc_info())
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


def list_return(index_list, definition):
    result_list = []
    for index in index_list:
        obj = scripts(index=index, only_status=False, df_return=True)
        func = "scripts." + definition + "(self)"
        res = getattr(obj, definition)()
        if len(res.index) > 0:
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
    return return_df


class scripts:
    def __init__(self, index=0, only_status=False, index_list=None, df_return=True):
        self.name = "nmd" + str(index)
        self.client_objects = ("buy_I_Volume, buy_N_Volume, buy_CountI, "
                               "buy_CountN, sell_I_Volume, sell_N_Volume, "
                               "sell_CountI, sell_CountN")
        self.closing_objects = ""
        self.best_limits_objects = ("datetime, number, qTitMeDem, zOrdMeDem, "
                                    "pMeDem, pMeOf, zOrdMeOf, qTitMeOf")
        self.day = tse_time.today_str(history=False)
        self.time = tse_time.current_time_str()[:3]
        self.sql_search = my_sql.search.script
        self.schema = my_sql.schemas
        self.only_status = only_status
        self.index_list = index_list
        self.df_return = df_return

    def return_process(self, schema, script):
        return_object = self.sql_search(schema=schema, script=script, df_return=self.df_return)
        if self.only_status is True:
            # when dataframe
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

    def latest_ghodrat_kh_ha(self):
        #client objects live
        script = ("select * from " + self.name + (" where buy_CountI < sell_CountI and"
                                                  " buy_I_Volume/buy_CountI > sell_I_Volume/sell_CountI"
                                                  " and finalLastDate LIKE " + self.day +
                                                  " and lastHEven LIKE " + "'" + self.time + "%'"))
        return scripts.return_process(self, self.schema.live_moneymaker(self), script=script)

    def latest_minute_best_limit(self):
        script = ("select " + self.best_limits_objects + " from " +
                  self.name + (" where qTitMeDem/zOrdMeDem > " +
                               "qTitMeOf/zOrdMeOf and datetime between NOW() -" +
                               " INTERVAL 1 MINUTE AND NOW()"))
        return scripts.return_process(self, self.schema.best_limits(self), script=script)

    def close_best_limit(self):
        script = ("select " + self.best_limits_objects +
                  " from " + self.name +
                  " where zOrdMeDem >" +
                  " ((zOrdMeOf)*3) and"
                  " qTitMeDem/zOrdMeDem > "
                  " (qTitMeOf/zOrdMeOf)*3" +
                  " ORDER BY datetime DESC"
                  " LIMIT 1")
        return scripts.return_process(self, self.schema.best_limits(self), script=script)
