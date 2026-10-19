
from django.urls import path
from .views import (shop_index,GroupsListView,ProfuctListView,
                    OrderListView,create_product,create_order,ShopIndexView,
                    ProductDetailViews,OrderDetailtView,ProductCreateView,
                    ProductUpdateView,ProductDelateView,OrderCreateView,
                    OrdertDelateView,OrderUpdateView)


app_name = 'shopapp'

urlpatterns = [
    path('',ShopIndexView.as_view(),name='index'),
    path("groups/",GroupsListView.as_view(),name='groups_list'),
    path('products/',ProfuctListView.as_view(),name='products_list_url'),
    path('products/create/',ProductCreateView.as_view(),name='product_create_url'),
    path('products/<int:pk>',ProductDetailViews.as_view(),name='product_details_url'),
    path('products/<int:pk>/update/',ProductUpdateView.as_view(),name='product_update_url'),
    path('products/<int:pk>/delete/',ProductDelateView.as_view(),name='product_delete_url'),


    path('orders/',OrderListView.as_view(),name='orders_list_url'),
    path('orders/create/',create_order,name='order_create_url'),
    path('orders/<int:pk>/',OrderDetailtView.as_view(),name='order_details_url'),
    path('orders/create/',OrderCreateView.as_view(),name='order_create_url'),
    path('orders/<int:pk>/update/',OrderUpdateView.as_view(),name='order_update_url'),
    path('orders/<int:pk>/delete/',OrdertDelateView.as_view(),name='order_delete_url'),
]
