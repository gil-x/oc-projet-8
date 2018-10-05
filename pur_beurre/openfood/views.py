from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Product, Category, Position
from .forms import SearchForm
from django.db.models import Q
import requests
import json

def get_products(request):
    """
    This view provides a JSON set of products of all grades but A.
    Used by jQuery autocomplete to suggests registered products.
    """
    if request.is_ajax():
        q = request.GET.get('term', '')
        print("x" + q + "x")
        products = Product.objects.filter(
            Q(product_name__startswith = q) &
            (Q(grade='e') | Q(grade='d') | Q(grade='c') | Q(grade='b'))
            ).order_by('product_name')[:10]
        results = []
        
        for product in products:
            results.append(product.product_name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def search_product(request):
    context = {}
    form = SearchForm(request.POST or None)
    context['form'] = form
    
    if form.is_valid(): 
        user_search = form.cleaned_data['search']
        context['search'] = user_search
        matching_products = Product.objects.filter(product_name__icontains=context['search'])

        if matching_products:
            context['result'] = matching_products[0]
            return HttpResponseRedirect(reverse(product_substitutes, kwargs={'pk': matching_products[0].pk}))
        else:
            # Let's see on OFF...
            # user_search
            return HttpResponseRedirect(reverse(search_on_off, kwargs={'search': user_search}))
            # return render(request, 'openfood/index.html', context)
    else:
        return render(request, 'openfood/index.html', context)


def search_on_off(request, search):
    context = {}
    context['user_search'] = search

    url="https://fr.openfoodfacts.org/cgi/search.pl"

    args = {
            'action': "process",
            # 'tagtype_0': "labels",
            'search_terms': search,
            # 'tag_contains_0': "contains",
            # 'tag_0': search,
            # 'sort_by': 'unique_scans_n',
            'json': 1,
            'page_size': 10,
            }
    response = requests.get(url, params=args)
    # products = response.json()["products"]

    # print("=====")
    # print(products)
    # print("=====")
    products = []

    for product in response.json()["products"]:
        try:
            products.append(product['product_name'])
        except KeyError:
            pass

    context['products'] = products


    return render(request, 'openfood/search_on_off.html', context)


    
def product_substitutes(request, pk):
    context = {}
    context['product'] = Product.objects.get(pk=pk)
    categories = context['product'].categories.all()
    positions = Position.objects.filter(product=context['product'])

    categories_and_rank = []
    for category in categories:
        categories_and_rank.append(
            (category.category_name, category.position_set.get(
                category=category, product=context['product']))
            )

    for category, rank in categories_and_rank:
        substitutes = Category.objects.filter(
            category_name=category).first().products.all().filter(
            Q(grade="a") | Q(grade="b")).order_by('?')
        if substitutes.count() != 0:
            context['substitutes'] = substitutes
            break

    if substitutes.count() == 0:
        context['substitutes'] = ["rien"] # TODO The template should returns Error...

    return render(request, 'openfood/product.html', context)


def ramdom_product(request):
    product_e = Product.objects.filter(grade='e').order_by('?').first()
    return HttpResponseRedirect(reverse(product_substitutes, kwargs={'pk': product_e.id}))
