from django.shortcuts import render
import importlib
import sys
from django.db import connections
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, best_limits, nmd46348559193224090
import calendar
from .external_models import ExternalData
from .templatetags import test_django

#tse_analize = importlib.import_module(r"E/rogramming/projects/python/Moneymaker/Moneymaker/Python/tse_analize")
#my_sql = importlib.import_module(r"E/rogramming/projects/python/Moneymaker/Moneymaker/Python/my_sql")
def all_events(request):
    event_list = Event.objects.all()
    return render(request, 'tset/event_list.html',
                  {'event_list': event_list})
def close_best_3(request):
    df_html = test_django.pd_to_html2()
    return render(request, 'tset/close_best.html', {'external_data': df_html})
def close_best(request):
    event_list = Event.objects.all()
    return render(request, 'tset/close_best.html',
                  {})

def external_data_view(request):
    with connections['external_db'].cursor() as cursor:
        # Run a raw SQL query
        cursor.execute("SELECT * FROM nmd46348559193224090")
        rows = cursor.fetchall()

    # Convert the result to a list of dictionaries for easy use in templates
    external_data = [{'datetime': row[0], 'number': row[1],
                      'qTitMeDem': row[2], 'zOrdMeDem': row[3],
                      'pMeDem': row[4], 'pMeOf:': row[5],
                      'zOrdMeOf': row[6], 'qTitMeOf': row[7]} for row in rows]

    return render(request, 'tset/close_best.html', {'external_data': external_data})

def history(request):
    with connections['external_manager'].cursor() as cursor:
        # Run a raw SQL query
        cursor.execute("SELECT namad_index,name FROM tblnamadha")
        rows = cursor.fetchall()

    # Convert the result to a list of dictionaries for easy use in templates
    external_data = [{'name': row[1], 'index': row[0]} for row in rows]

    return render(request, 'tset/history.html', {'external_data': external_data})


def history_detail_view(request, index):
    df_html = test_django.history_to_html(index, "moneymaker")
    return render(request, 'tset/history_index.html', {'external_data': df_html})

def financial_records_view(request):
    # Fetch all financial records from the database
    records = nmd46348559193224090.objects.all()
    # Pass data to the template
    return render(request, 'tset/close_best.html', {'records': records})


def close_best_2(request):
    data = best_limits.get_related_articles.raw("select * from nmd46348559193224090")
    return render(request, 'tset/close_best.html', {'data': data})

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "John"
    month = month.capitalize()
    # convert month from names to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar

    cal = HTMLCalendar().formatmonth(
        year,
        month_number)
    # get current year
    now = datetime.now()
    current_year = now.year
    time = now.strftime('%I:%M %p')
    return render(request,
                  "tset/home.html", {
                      "name": name,
                      "year": year,
                      "month": month,
                      "month_number": month_number,
                      "cal": cal,
                      "current_year": current_year,
                      "time": time,
                  })
