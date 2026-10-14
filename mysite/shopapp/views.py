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
from .models import Product,Order

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
class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'shopapp/orders-list.html'
    #queryset = (
    #   Order.objects.select_related("user")
    #    .prefetch_related('products')
    #)
    
    context_object_name = 'orders'
    paginate_by = 10  # Показывать по 10 заказов на одной странице

    def get_queryset(self):
        """Возвращает только заказы текущего авторизованного пользователя."""
        # Используем prefetch_related, чтобы оптимизировать запросы к БД (избежать проблемы N+1)
        # и сразу подгрузить связанные позиции и товары одной выборкой.
        return (
            Order.objects.filter(user=self.request.user)
            .prefetch_related('items__product')
            .order_by('-created_at')  # Сначала новые заказы
        )

    