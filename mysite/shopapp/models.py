from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy,ngettext
from decimal import Decimal
from django.db.models import Sum, F

class Category(models.Model):
  name = models.CharField(max_length=100, verbose_name='Название категории')
  slug = models.SlugField(max_length=100, unique=True, verbose_name='URL',null=True)

  class Meta:
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'
    ordering = ['name']

  def __str__(self):
    return self.name



# Create your models here.
class Product(models.Model):

    """
    Product  представляет товар

    Заказы: :model:'shopapp.Order'
    """
    
    class Meta:
        # сортировка по имени
        ordering = ['name','price']
        # по какой таблице искать
        #db_table = "tech_products"
        # как обьявлять во множественном числе
        #verbose_name_plural = "products"
        verbose_name = _('Product')
        
    name = models.CharField(max_length=100,db_index=True)
    category = models.ForeignKey(Category,null=True,
      related_name='products',
      on_delete=models.CASCADE,
      verbose_name='Категория',
  )
    description = models.TextField(null=False,blank=True,db_index=True)
    price = models.DecimalField(default=0,max_digits=8,decimal_places=2,
                                validators=[MinValueValidator(0)])
    discount = models.PositiveSmallIntegerField(default=0,
                                                validators=[
                                                    MaxValueValidator(100)
                                                ])
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    archived = models.BooleanField(default=False)


    @property
    def description_short(self) ->str:

        if len(self.description) < 48:
            return self.description
        return self.description[:48]+'...'

    def __str__(self):
        return f"Product (pk={self.pk} name={self.name})"

    @property
    def discount_price(self):
        """Возвращает стоимость товара с учетом скидки в процентах."""
        if self.discount > 0:
            discount_amount = (self.price * self.discount) / 100
            return self.price - discount_amount
        return self.price

    def __str__(self):
        return self.name


class Order(models.Model):

    class Meta:
        # сортировка по имени
        # ordering = ['user','products']
        # по какой таблице искать
        #db_table = "tech_orderss"
        # как обьявлять во множественном числе
        # verbose_name_plural = "orders"
        verbose_name = _('Order')


    delivery_address = models.TextField(null=True,blank=True)
    promocode = models.CharField(max_length=20,null=False,blank=True)
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    products = models.ManyToManyField(Product,related_name='orders')

    receipt = models.FileField(null=True,upload_to='orders/receipts')