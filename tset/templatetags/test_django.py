from django import template
import mariadb
import pandas as pd
from sqlalchemy import create_engine
from Engine import tse_analize, my_sql

register = template.Library()


def convert_data_frame_to_html_table_headers(df):
    html = "<tr>"
    for col in df.columns:
        html += f"<th>{col}</th>"
        html += "</tr>"
        return html


def convert_data_frame_to_html_table_rows(df):
    html = ""
    for row in df.values:
        row_html = "<tr>"
        for value in row:
            row_html += f"<td>{value}</td>"
        row_html += "</tr>"
    html += row_html
    return html


register.filter("convert_data_frame_to_html_table_rows", convert_data_frame_to_html_table_rows)
register.filter("convert_data_frame_to_html_table_headers", convert_data_frame_to_html_table_headers)


def script():
    try:
        # baz kardane sql va khandane tblnamadhatemp
        engine = create_engine("mariadb+mariadbconnector://root:Unique2213@127.0.0.1:3306"
                               "/best_limits")
        query = "select * from nmd46348559193224090"
        df = pd.read_sql(query, engine)
        return df
    except:
        return None


def pd_to_html():
    try:
        index_list = my_sql.read.index(bl_check=True)
        df = tse_analize.dataframe_return(index_list, "close_best_limit")
        df_html = df.to_html(justify="center", classes="table table-bordered")
        return df_html
    except:
        return None


def pd_to_html2(live=True):
    try:
        df = tse_analize.django_temp(live=live)
        df_html = df.to_html(justify="center", classes="table table-bordered")
        return df_html
    except:
        return None


def history_to_html(index, schema):
    try:
        df = my_sql.read.all_tables(index, schema)
        df_html = df.to_html(justify="center", classes="table table-bordered")
        return df_html
    except:
        my_sql.log.error_write("")
        return None

def close_best_limit_tohtml(index, schema):
    try:
        df = my_sql.read.all_tables(index, schema)
        df_html = df.to_html(justify="center", classes="table table-bordered")
        return df_html
    except:
        my_sql.log.error_write("")
        return None
