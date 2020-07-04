from django.shortcuts import render, redirect
from .models import Product, Listing, Comment, CustomUser, Gallery, Transaction, Category
from users.models import UserAddress
from users.views import userProfileView
from .forms import CreateListingForm, CommentForm, TransactionForm
from users.forms import ChangeAddressForm
from django.forms import ModelForm, ValidationError
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

def userHome(request):
    listings = Listing.objects.filter(seller=request.user.id)
    purchased = Transaction.objects.filter(buyer=request.user.id)
    sold = Transaction.objects.filter(seller=request.user.id)

    context = {
        'listings': listings,
        'purchased': purchased,
        'sold': sold,
        }
    return render(request, 'user_home.html', context)

def productCategoryView(request, the_slug):
    category_current = Category.objects.get(slug=the_slug)
    breadcrum = category_current.get_ancestors(ascending=False, include_self=True)
    children = category_current.get_descendants(include_self=True)
    categories = category_current.get_descendants()

    selected_listings = Listing.objects.select_related('seller').filter(category__in=children)
    sold_listings = selected_listings.filter(status=4)
    active_listings = selected_listings.filter(status=1)


    context = {
        'active_listings': active_listings,
        'sold_listings': sold_listings,
        'breadcrum': breadcrum,
        'categories': categories,
        'category_current': category_current,
    }
    return render(request, 'product_category.html', context)

def productDetail(request, slug):
    products = Product.objects.filter(category__slug=slug)
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
            return redirect('product-listing', listing_id=listing.id)
    else:
        form = CreateListingForm(initial={'seller':request.user.id, 'status':2})
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
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    gallery = Gallery.objects.filter(listing=listing_id)
    buyer = request.user
    seller = listing.seller

    if listing.status == 4:
        return redirect('product-listing', listing_id)

    try:
        user_address = UserAddress.objects.get(user__id=user.id)
        form_address = ChangeAddressForm(instance=user_address)
    except UserAddress.DoesNotExist:
        user_address = None
        form_address = ChangeAddressForm()

    form = TransactionForm(initial={
    'buyer': buyer,
    'listing': listing,
    'seller': seller,
    'status': 1
        })

    if request.method == "POST":
        if 'set_useraddress' in request.POST:
            form_address = ChangeAddressForm(data=request.POST, instance=user_address)
            if form_address.is_valid():
                # To save the object, save the instance object, not the form.
                obj = form_address.save(commit=False)
                obj.user = user
                obj.save()
                return redirect('buy-listing', listing_id=listing_id)
        elif 'transaction' in request.POST:
            form = TransactionForm(data=request.POST, status=listing.status, address=user_address)
            if form.is_valid():
                form.save()
                return redirect('buy-transaction', listing_id=listing_id)

    context = {
        'listing': listing,
        'gallery': gallery,
        'user_address': user_address,
        'form': form,
        'form_address': form_address,
    }
    return render(request, 'buy-listing.html', context)

def transaction(request, listing_id):
    buyer = request.user
    listing = Listing.objects.get(id=listing_id)
    seller = listing.seller

    if request.method == "POST":
        form = TransactionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('buy-transaction')
    else:
        form = TransactionForm(initial={
            'buyer': buyer,
            'listing': listing,
            'seller': seller,
            })

    context = {
        'form': form,
        'listing': listing
    }
    return render(request, 'buy-transaction.html', context)

def shopHome(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'shop-home.html', context)