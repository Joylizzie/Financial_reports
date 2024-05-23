from django.urls import path

from  finreports import views

urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"),
    path("", views.index, name="index"),
    path("balancesheet/", views.balancesheet, name="bs"),
    path("pl/", views.pl, name="pl"),
    path("araging/", views.araging, name="araging"),
]