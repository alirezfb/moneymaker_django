from django.urls import path
from . import views

urlpatterns = [
    # path:whole urls /
    # slug:hypen-and_underscore_stuff
    # UUID:Universally unique identifier

    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
]
