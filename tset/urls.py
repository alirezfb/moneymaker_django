from django.urls import path
from . import views

urlpatterns = [
    # path:whole urls /
    # slug:hypen-and_underscore_stuff
    # UUID:Universally unique identifier

    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events', views.all_events, name="list_events"),
    path('best', views.close_best_3, name="close_best_3"),
    path('history/indexlist', views.history, name="history"),
    path('history/<int:index>/', views.history_detail_view, name='index_history'),
]
