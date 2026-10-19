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
from .forms import GroupForm,ProductForm,OrderForm
from .models import Product,Order

# Create your views here.

class ShopIndexView(View):
    def get(self,request:HttpRequest) ->HttpResponse:

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
#   PRODUCTS LIST
########################################################################################   
#class ProfuctListView(TemplateView):
#    template_name = 'shopapp/products-list.html'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['products1'] = Product.objects.all()
#        return context


class ProfuctListView(ListView):
    template_name = 'shopapp/products-list.html'
    # отображаются все продукты
    model = Product
    context_object_name = 'products1'
    # не отображаются архивные продукты
    queryset = Product.objects.filter(archived=False)

####################################################################
# Product Create
#################################################################################
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['products1'] = Product.objects.all()
    #    return context    

#class ProductCreateView(UserPassesTestMixin,CreateView):
    # проверка может ли пользователь создавать заказ
    #def test_func(self):
        #return self.request.user.groups.filter(name='secret-group').exists()
    #    return self.request.user.is_superuser
    #model = Product
    #fields = 'name','price','description','discount','category'
    #form = ProductForm() 
    # шаблон должен называться product_form.html
    #success_url = reverse_lazy('shopapp:products_list_url')

    #def form_valid(self, form):
    #    form.instance.created_by = self.request.user
    #    response = super().form_valid(form)
    #    return response

#################################################################
# Product Detail
############################################################################
class ProductDetailViews(DetailView):
    template_name = 'shopapp/product-details.html'
    #model = Product
    queryset = Product.objects.prefetch_related()
        # не отображаются архивные продукты
    queryset = Product.objects.filter(archived=False)
    context_object_name = 'product'


#class ProductDetailViews(View):
#    def get(self,request:HttpRequest,pk:int)->HttpResponse:
#        product = get_object_or_404(Product,pk=pk)
#        context = {
#            'product':product
#        }
#        return render(request,'shopapp/product-details.html',context)


    #template_name = 'shopapp/product-details.html'
    # model = Product
    #queryset = Product.objects.prefetch_related('images')
    #context_object_name = 'prod'



def create_product(request:HttpRequest)->HttpResponse:
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
           
            #Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse('shopapp:products_list_url')
            return redirect(url)
    
    
    else:
        form = ProductForm()
        context = {
            'form':form,
        }
    return render(request,'shopapp/create-product.html',context=context)

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

##############################################################
#Product create
#######################################################

class ProductCreateView(CreateView):
    # проверка может ли пользователь создавать заказ
    #def test_func(self):
        #return self.request.user.groups.filter(name='secret-group').exists()
        #return self.request.user.is_superuser
    model = Product
    fields = 'name','price','description','discount','category'
    #form = ProductForm 
    # шаблон должен называться product_form.html
    success_url = reverse_lazy('shopapp:products_list_url')

    #def form_valid(self, form):
    #    form.instance.created_by = self.request.user
    #    response = super().form_valid(form)
    #    return response    
#####################################################################################
#Product update
####################################################

class ProductUpdateView(UpdateView):
    model = Product
    # fields = 'name','price','description','discount','prewiew'
    # template_name = ''
    form_class = ProductForm
    template_name_suffix = '_update_form'
    context_object_name = 'prod_det'

    def get_success_url(self):
        return reverse(
            "shopapp:product_details_url",
            kwargs={"pk":self.object.pk},
        )

    #def form_valid(self, form):
    #    response = super().form_valid(form)
    #    for image in form.files.getlist('images'):
    #        ProductImage.objects.create(
    #           product = self.object,
    #           image=image
    #        )
    #    return response

#################################################################################
#Product delete
##################################################################################
class ProductDelateView(DeleteView):
    # для удаления
    model = Product
    success_url = reverse_lazy('shopapp:products_list_url')

    # для архивации добавим функцию
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

##################################################################################
# Orders details
# ##################################################################################

# просмотр деталей заказа не всем пользователям
class OrderDetailtView(PermissionRequiredMixin,DetailView):
    permission_required = ['view_order'] # просмотр деталей заказа не всем пользователям
    queryset = (
       Order.objects.select_related("user")
        .prefetch_related('products')
    )
    context_object_name = 'order'

#########################################################################################################
#ORDERS LIST
#############################################################################

# LoginRequiredMixin просмотреть заказы можно только после login
class OrderListView(ListView):
    template_name = 'shopapp/orders-list.html'
        # отображаются все продукты
    model = Order
    queryset = Order.objects.all()
    context_object_name = 'orders'


class ProfuctListView(ListView):
    template_name = 'shopapp/products-list.html'
    # отображаются все продукты
    model = Product
    context_object_name = 'products1'
    # не отображаются архивные продукты
    queryset = Product.objects.filter(archived=False)    


class OrderCreateView(CreateView):
        # шаблон должен называться order_form.html
    model = Order
    fields = 'delivery_address','promocode','user','products'
    success_url = reverse_lazy('shopapp:orders_list_url')

class OrderUpdateView(UpdateView):
    model = Order
    fields = 'delivery_address','promocode','user','products'  
    template_name_suffix = '_update_form'
    context_object_name = 'order_upd'
    # success_url = reverse_lazy('shopapp:products_list_url')

    # для того чтобы вернутся к продукту нужно сделать get_succsess_url
    def get_success_url(self):
        return reverse(
            'shopapp:order_details_url',
            kwargs={"pk":self.object.pk},
        ) 
    

class OrdertDelateView(DeleteView):
    # для удаления
    model = Order
    success_url = reverse_lazy('shopapp:orders_list_url')
    



def create_order(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
         form = OrderForm(request.POST) #валидность 
         if form.is_valid():
            # name = form.cleaned_data['name']
            # price = form.cleaned_data['price']
            # description = form.cleaned_data['description']
            
            # Product.objects.create(**form.cleaned_data) # **для распакрвки
            form.save()
            url = reverse('shopapp:orders_list_url')
            return redirect(url)
    else:     
        form = OrderForm()
    context = {
        'form':form
    }
   
    return render(request,'shopapp/create-order.html',context=context)
    