from django.shortcuts import (render,redirect,reverse,get_object_or_404,)
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from timeit import default_timer
from django.contrib.auth.models import Group,User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView,
                                  UpdateView,)
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        UserPassesTestMixin)
from .forms import GroupForm
from .models import Product,Order,OrderItem

# Create your views here.
def shop_index(request:HttpRequest):

    cars =[
        ("BMW", 120000,'$'),
        ("Audi", 125000,'$'),
        ("Mersedes Bance", 155000,'$'),
         
    ]

    context = {
        "time_running":default_timer(),
        'cars':cars
    }
    return render(request,'shopapp/shop-index.html',context=context)


class GroupsListView(View):
    def get(self,request:HttpRequest) ->HttpResponse:
            context = {
                'form':GroupForm,
            'groupsss': Group.objects.prefetch_related('permissions').all() # для html легче грузить
            }
            return render(request,"shopapp/groups-list.html",context=context)

    def post(self,request:HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)

################################################################################# 
#   PRODUCTS
########################################################################################   
class ProfuctListView(ListView):
    template_name = 'shopapp/products-list.html'
    # отображаются все продукты
    # model = Product
    context_object_name = 'products1'
    # не отображаются архивные продукты
    queryset = Product.objects.filter(archived=False)

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['products1'] = Product.objects.all()
    #    return context    



######################################################################################
#   ORDERS
#################################################################################
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order

#class OrderListView(LoginRequiredMixin, ListView):
    #model = Order
    #template_name = 'shopapp/orders-list.html'  # Путь к вашему шаблону списка заказов
    #context_object_name = 'orders'            # Имя переменной со списком заказов в шаблоне
    #ordering = ['-created_at']                # Сортировка: сначала новые заказы

    #def get_queryset(self):
        #user = self.request.user
        #queryset = super().get_queryset()

        # 1. Если пользователь — админ или менеджер (is_staff), отдаем вообще ВСЕ заказы.
        # 2. Если обычный пользователь — фильтруем только по его заказам.
        #if not user.is_staff:
         #   queryset = queryset.filter(user=user)

        # Обязательно оставляем prefetch_related для защиты от N+1 запросов к БД
        #return queryset.prefetch_related('items__product')


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/orders-list.html'
    context_object_name = 'orders'
    ordering = ['-created_at']

    def get_queryset(self):
        # 1. Фильтруем заказы: показываем только заказы текущего пользователя
        # 2. prefetch_related('items__product') подтягивает все OrderItem и связанные Product 
        #    за один дополнительный запрос, чтобы база данных не "ложилась" от нагрузки
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related('items__product')
            .order_by('-created_at')
        )