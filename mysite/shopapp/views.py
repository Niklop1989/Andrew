from django.shortcuts import render
from timeit import default_timer
from django.http import HttpRequest,HttpResponse


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