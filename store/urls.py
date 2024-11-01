from django.urls import path

from . import views

urlpatterns = [
    path("add_product/", views.add_product, name="add_product"),
    path("buy_product/", views.buy_product, name="buy_product"),
]
