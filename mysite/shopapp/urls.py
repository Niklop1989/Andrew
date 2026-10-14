
from django.urls import path
from .views import (shop_index,GroupsListView,ProfuctListView,
                    OrderListView)


app_name = 'shopapp'

urlpatterns = [
    path('',shop_index,name='index'),
    path("groups/",GroupsListView.as_view(),name='groups_list'),
    path('products/',ProfuctListView.as_view(),name='products_list_url'),
    path('orders/',OrderListView.as_view(),name='orders_list_url'),
]
