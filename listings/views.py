from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from listings.choices import bedroom_choices, state_choices, price_choices

from .models import Listing

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True) #filter out anything not published.

    paginator = Paginator(listings, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
    }

    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):

    # 404s if non-existent.
    listing = get_object_or_404(Listing, pk=listing_id) # listing_id passed in through url

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)

def search(request):

    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list.filter(description__icontains=keywords) # icontains is not case sensitive

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list.filter(description__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list.filter(description__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list.filter(description__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list.filter(description__lte=price)

    context = {
        'state_choices' : state_choices,
        'bedroom_choices' : bedroom_choices,
        'price_choices' : price_choices,
        'listings' : queryset_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)