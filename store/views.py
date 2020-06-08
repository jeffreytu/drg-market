from django.shortcuts import render
from .models import Product, Listing
from .forms import CreateListingForm
from django.forms import ModelForm, ValidationError
# Create your views here.

def userHome(request):
    listings = Listing.objects.filter(seller=request.user.id)
    products = Listing.objects.exclude(seller=request.user.id)
    context = {
        'listings': listings,
        'products': products,
        }
    return render(request, 'user_home.html', context)

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
        form = CreateListingForm(data=request.POST, user=request.user)
        # if form.is_valid():
            # if form.cleaned_data['seller'] == request.user:
                # form.save()
            # else:
            #     print(form.errors)
            #     print(form.non_field_errors)
    else:
        form = CreateListingForm(initial={'seller':request.user.id})
    context = {'form': form}
    return render(request, 'sell.html', context)