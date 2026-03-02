from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("send/", views.send_view, name="send"),
    path("search/", views.search_view, name="search"),
    path("statistics/", views.statistics_view, name="statistics"),
]
