from django.contrib import admin

# Register your models here.
from io import TextIOWrapper
from csv import DictReader


from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from .models import Product,Category,Order



class ProductInline(admin.TabularInline): #StackedInline
    model = Order.products.through

@admin.action(description='Archivrd products')
def mark_archived(modeladmin: admin.ModelAdmin,request:HttpRequest,queryset:QuerySet):
    queryset.update(archived=True)

@admin.action(description='Unarchivrd products')
def mark_unarchived(modeladmin: admin.ModelAdmin,request:HttpRequest,queryset:QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv"
    ]

    #list_display = "pk",'name','price','discount','description'
    list_display = "pk",'name','category','price','discount','description_short','discount_price','archived'
    list_display_links = 'pk','name'
    ordering = ['name','price']
    search_fields = 'name','description'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):    
    list_display = "pk",'name','slug'



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'delivery_address','promocode','created_at','user_verbose'
    inlines = [
        ProductInline
    ]
    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')
    
    def user_verbose(self, obj:Order) -> str:
        return obj.user.first_name,obj.user.last_name or obj.user.username    