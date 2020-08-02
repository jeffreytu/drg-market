from django.shortcuts import render, redirect
from django.db.models import Avg, Min
from .models import Product, Listing, Comment, CustomUser, Gallery, Transaction, Category
from users.models import UserAddress
from users.views import userProfileView
from .forms import CreateListingForm, CommentForm, TransactionForm
from users.forms import ChangeAddressForm
from django.forms import ModelForm, ValidationError
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.http import JsonResponse
import random, string, json
from django.core.serializers.json import DjangoJSONEncoder

def userHome(request):
    listings = Listing.objects.filter(seller=request.user.id)
    transactions = Transaction.objects.select_related('listing')
    purchased = transactions.filter(buyer=request.user.id)
    sold = transactions.filter(seller=request.user.id)

    context = {
        'listings': listings,
        'purchased': purchased,
        'sold': sold,
        }
    return render(request, 'user_home.html', context)

def userView(request, seller):
    viewer = request.user
    seller_profile = CustomUser.objects.get(username=seller)
    listings = Listing.objects.filter(seller__username=seller)
    context = {
        'seller': seller_profile,
        'listings': listings,
    }
    return render(request, 'view_user.html', context)

def productCategoryView(request, the_slug):
    category_current = Category.objects.get(slug=the_slug)
    breadcrum = category_current.get_ancestors(ascending=False, include_self=True)
    children = category_current.get_descendants(include_self=True)
    categories = category_current.get_descendants()

    for child in categories:
        child_listings = Listing.objects.filter(category=child).filter(status=1).aggregate(avg_price=Min('price'))
        child.avg_price = child_listings.get('avg_price')

    selected_listings = Listing.objects.select_related('seller').filter(category__in=children)
    sold_listings = selected_listings.filter(status=4)
    active_listings = selected_listings.filter(status=1)

    for listing in active_listings:
        try:
            seller_location = UserAddress.objects.get(user=listing.seller)
            listing.location = seller_location.city + ", " + seller_location.state
        except:
            listing.location = None

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
    slug = listing.category.slug
    comments = Comment.objects.filter(listing=listing_id)
    gallery = Gallery.objects.filter(listing=listing_id)
    category_current = Category.objects.get(slug=slug)
    breadcrum = category_current.get_ancestors(ascending=False, include_self=True)
    user = request.user

    try:
        seller_location = UserAddress.objects.get(user=listing.seller)
        listing.location = seller_location.city + ", " + seller_location.state
    except:
        listing.location = None

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
        'breadcrum': breadcrum,
    }

    return render(request, 'product_listing.html', context)

def editListing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    gal = Gallery.objects.filter(listing=listing_id).prefetch_related('listing')
    gallery = gal.values('image')
    

    if request.method == 'GET':
        form = CreateListingForm(instance=listing)
    elif request.method == 'POST':
            form = CreateListingForm(data=request.POST, instance=listing, user=request.user, files=request.FILES)
            if request.POST.get('request') == 'delete':
                image = Gallery.objects.get(image=request.POST.get('name'))
                image.delete()
            else:
                files = request.FILES.getlist('gallery')

                if form.is_valid():
                    if len(files) > 0:
                        editlisting = form.save(commit=False)
                        for f in files:
                            gallery = Gallery(listing=editlisting, image=f)
                            gallery.save()
                            editlisting.save()
                    else:
                        form.save()
                    return redirect('edit-listing', listing_id=listing_id)
    context = {
        'form': form,
        'listing': listing,
        'e_gallery': json.dumps(list(gallery))
        }
    return render(request, 'product_listing_edit.html', context)

def createListing(request):

    if request.method == 'POST':
        form = CreateListingForm(data=request.POST, user=request.user, files=request.FILES)
        the_files = request.FILES

        if form.is_valid():
            listing = form.save(commit=False)
            listing.listing_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            listing.gallery = the_files
            listing.save()

            if the_files:
                for f in the_files:
                    gallery = Gallery(listing=listing, image=the_files[f])
                    gallery.save()
            return JsonResponse({'listing':listing.id})
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

def shopPhones(request):
    categories = Category.objects.select_related('parent').all()
    iphones = categories.get(slug='apple-iphone').get_children()
    samsungs = categories.get(slug='samsung').get_children()

    context = {
        'iphones': iphones,
        'samsungs': samsungs,
    }
    return render(request, 'shop_phones.html', context)