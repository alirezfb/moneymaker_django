from django import template
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


def pd_to_html():
    try:
        index_list = my_sql.read.index(bl_check=True)
        df = tse_analize.dataframe_return_old(index_list, "close_best_limit")
        df_html = df.to_html(justify="center", classes="table table-bordered")
        return df_html
    except:
        return None
