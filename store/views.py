from django.shortcuts import render
from .models import Product
# Create your views here.

def productList(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

def productDetail(request, sku):
    product = Product.objects.get(sku=sku)
    context = {'product': product}
    return render(request, 'product_detail.html', context)