from django.shortcuts import render
from .models import Product
# Create your views here.

def productList(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

def productDetail(request):
    print('product detail')
    return render(request, 'product_list.html', context)