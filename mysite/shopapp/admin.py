from django.contrib import admin

# Register your models here.
from io import TextIOWrapper
from csv import DictReader
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from .models import Product,Category,Order,OrderItem

class OrderItemInline(admin.TabularInline):
    """Позволяет добавлять и редактировать товары прямо внутри заказа."""
    model = OrderItem # Раскомментируйте и укажите вашу промежуточную модель
    extra = 1
    raw_id_fields = ('product',)  # Удобный поиск товара по ID (полезно, если товаров много)


class ProductInline(admin.TabularInline): #StackedInline
    model = Order.products.through

@admin.action(description='Archivrd products')
def mark_archived(modeladmin: admin.ModelAdmin,request:HttpRequest,queryset:QuerySet):
    queryset.update(archived=True)

@admin.action(description='Unarchivrd products')
def mark_unarchived(modeladmin: admin.ModelAdmin,request:HttpRequest,queryset:QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin,ExportAsCSVMixin):

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

    fieldsets = [
        ('none',{
            'fields':('name','description'),
        }),
        ('Price options',{
            'fields':('price','discount'),
            'classes':('collapse','wide'),
        }),

        ('Extra options',{
            'fields':('archived',),
            'classes':('collapse',),
            'description':'Extra options, field "archived" is soft delete',
        })
    ]


    def import_csv(self,request:HttpRequest) -> HttpResponse:
        from .common import save_csv_products
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                'form':form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST,request.FILES)
        if not form.is_valid():
            context = {
                'form':form,
            }
            return render(request, 'admin/csv_form.html', context,status=400)
        save_csv_products(
            form.files['csv_file'].file,
            encoding=request.encoding,
        )            
        self.message_user(request,'create csv file')
        return redirect("..")
            

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import-products-csv/",
                self.import_csv,
                name="import_products_csv",
            ),
        ]
        return new_urls + urls


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):    
    list_display = "pk",'name','slug'


@admin.register(Order) # Раскомментируйте, когда добавите модель Order
class OrderAdmin(admin.ModelAdmin):
    """Административная панель для управления заказами."""
    
    # Отображение полей в списке заказов
    list_display = ['delivery_address','user','display_products'] # Кастомное поле для отображения суммы
    
    @admin.display(description="Products")  # Задает имя колонки в админке
    def display_products(self, obj):
        # Собираем имена связанных продуктов через запятую
        return ", ".join([product.name for product in obj.products.all()])
    
    # Фильтры в правой колонке
    #list_filter = 'created_at'
    
    # Поля, по которым доступен поиск
    search_fields = ('id', 'delivery_address')
    
    # Иерархия по датам для быстрой навигации
    date_hierarchy = 'created_at'
    
    # Подключение inline-редактирования товаров внутри заказа
    inlines = [OrderItemInline]
    
    # Группировка полей внутри формы редактирования заказа
    fieldsets = (
        (None, {
            'fields': ('user','products',)
        }),
        ('Информация о доставке', {
            'fields': ('delivery_address', 'promocode',),
            'classes': ('collapse',),  # Сворачиваемый блок
        }),
    )

    def total_cost_display(self, obj):
        """Отображает общую стоимость заказа в списке."""
        # Пример расчета, если у вас есть метод total_cost в модели Order
        # return f"{obj.total_cost()} руб."
        return "0.00 руб."
    
    total_cost_display.short_description = 'Общая стоимость'

    def save_related(self, request: HttpRequest, form, formsets, change):
        """
        Кастомный метод сохранения связанных данных.
        Полезен, если нужно пересчитать общую сумму заказа после сохранения товаров.
        """
        super().save_related(request, form, formsets, change)
        # Пример логики пересчета:
        # order = form.instance
        # order.update_total_price() 