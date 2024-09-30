from django.contrib import admin
from .models import Venue
from .models import MoneymakerUser
from .models import Event

admin.site.register(Venue)
admin.site.register(MoneymakerUser)
admin.site.register(Event)

