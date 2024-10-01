from django.shortcuts import render
import importlib
import sys
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, best_limits
import calendar
tse_analize = importlib.import_module(r"E/rogramming/projects/python/Moneymaker/Moneymaker/Python/tse_analize")
my_sql = importlib.import_module(r"E/rogramming/projects/python/Moneymaker/Moneymaker/Python/my_sql")
def all_events(request):
    event_list = Event.objects.all()
    return render(request, 'tset/event_list.html',
                  {'event_list': event_list})
def close_best_3(request):
    index_list = my_sql.read.index(bl_check=True)
    df = tse_analize.list_return(index_list, "close_best_limit")
    dic = {
        "df": df.to_html()
    }
    print(dic)
    return render(request, 'tset/close_best.html', context=dic)
def close_best(request):
    event_list = Event.objects.all()
    return render(request, 'tset/close_best.html',
                  {})

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
