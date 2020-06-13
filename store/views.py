from django.shortcuts import render, redirect
from .models import Product, Listing, Comment, CustomUser
from .forms import CreateListingForm, CommentForm
from django.forms import ModelForm, ValidationError
from django.http import HttpResponseRedirect

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
    comments = Comment.objects.filter(listing=listing_id)
    user = request.user

    if request.method == 'POST':
        form = CommentForm(data=request.POST, user=user, listing=listing)
        if form.is_valid():
            body = request.POST.get('body')
            form = Comment.objects.create(author=user, listing=listing, body=body)
            form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    
    context = {
        'form': form,
        'comments': comments,
        'listing': listing,
    }

    return render(request, 'product_listing.html', context)

def editListing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == 'GET':
        form = CreateListingForm(instance=listing)
    elif request.method == 'POST':
            form = CreateListingForm(data=request.POST, instance=listing, user=request.user)
            files = request.FILES.getlist('file_field')
            if form.is_valid():
                form.save()
                return redirect('edit-listing', listing_id=listing_id)
    context = {'form': form}
    return render(request, 'product_listing_edit.html', context)

def createListing(request):
    if request.method == 'POST':
        form = CreateListingForm(data=request.POST, user=request.user)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            # for f in files:
            #     instance = Image(image=file)  # match the model.
            #     instance.save()
            form.save()
            return redirect('create-listing')
    else:
        form = CreateListingForm(initial={'seller':request.user.id})
    context = {'form': form}
    return render(request, 'sell.html', context)