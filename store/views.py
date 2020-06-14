from django.shortcuts import render, redirect
from .models import Product, Listing, Comment, CustomUser, Gallery
from .forms import CreateListingForm, CommentForm
from django.forms import ModelForm, ValidationError
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

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
    gallery = Gallery.objects.filter(listing=listing_id)

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
        'gallery': gallery,
    }

    return render(request, 'product_listing.html', context)

def editListing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    gallery = Gallery.objects.filter(listing=listing_id)
    if request.method == 'GET':
        form = CreateListingForm(instance=listing)
    elif request.method == 'POST':
            form = CreateListingForm(data=request.POST, instance=listing, user=request.user, files=request.FILES)
            files = request.FILES.getlist('gallery')
            if form.is_valid():
                editlisting = form.save(commit=False)
                for f in files:
                    gallery = Gallery(listing=editlisting, image=f)
                    gallery.save()
                editlisting.save()
                return redirect('edit-listing', listing_id=listing_id)
    context = {
        'form': form,
        'listing': listing,
        'gallery': gallery,
        }
    return render(request, 'product_listing_edit.html', context)

def createListing(request):
    if request.method == 'POST':
        form = CreateListingForm(data=request.POST, user=request.user, files=request.FILES)
        files = request.FILES.getlist('gallery')
        if form.is_valid():
            listing = form.save(commit=False)
            listing.save()
            if request.FILES:
                for f in files:
                    gallery = Gallery(listing=listing, image=f)
                    gallery.save()
            return redirect('create-listing')
    else:
        form = CreateListingForm(initial={'seller':request.user.id})
    context = {'form': form}
    return render(request, 'sell.html', context)

def deleteListing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == 'POST':
        listing.delete()
        return redirect('user-home')
    context = {
        'listing': listing
    }
    return render(request, 'product_listing_delete.html', context)

def buyListing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    gallery = Gallery.objects.filter(listing=listing_id)
    context = {
        'listing': listing,
        'gallery': gallery,
    }
    return render(request, 'buy-listing.html', context)