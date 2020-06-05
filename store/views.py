from django.shortcuts import render
from .models import Product, Listing
from .forms import CreateListingForm
# Create your views here.

def productList(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

def productDetail(request, sku):
    product = Product.objects.get(sku=sku)
    listings = Listing.objects.filter(category__sku=sku)
    context = {
        'product': product,
        'listings': listings
    }
    return render(request, 'product_detail.html', context)

def productListingDetail(request,listing_id):
    listing = Listing.objects.get(id=listing_id)
    context = {'listing': listing}
    return render(request, 'product_listing.html', context)

def createListing(request):
    seller = Listing.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = CreateListingForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['seller'] == request.user:
                form.save()
            else:
                print('invalid user submission')
    else:
        form = CreateListingForm(initial={'seller':request.user.id})
    context = {'form': form}
    return render(request, 'sell.html', context)