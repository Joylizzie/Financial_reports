from django.urls import path

from  araging import views

urlpatterns = [
    # path("", views.IndexView.as_view(), name="index"),
    path("", views.index, name="index"),
    #path("homepage/", views.homepage, name="homepage"),
    # path("databases", views.databases, name="databases"),
    # path("<customter_id>/", views.customers_view, name="customers_name_id"),
]