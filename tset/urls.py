from django.urls import path
from . import views

urlpatterns = [
    # path:whole urls /
    # slug:hypen-and_underscore_stuff
    # UUID:Universally unique identifier

    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events', views.all_events, name="list_events"),
    path('best', views.close_best, name="close_best_3"),
]
