from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event


def all_events(request):
    event_list = Event.objects.all()
    return render(request, 'tset/event_list.html',
                  {'event_list': event_list})

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
