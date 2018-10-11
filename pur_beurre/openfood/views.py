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
            return HttpResponseRedirect(reverse(product_substitutes, kwargs={
                'pk': matching_products[0].pk,
                # 'user_search': user_search,
                }))
        else:
            user_search = user_search.replace(" ", "-")
            return HttpResponseRedirect(reverse(search_on_off, kwargs={'search': user_search}))
    else:
        return render(request, 'openfood/index.html', context)


def search_on_off(request, search):
    context = {}
    context['user_search'] = search.replace("-", " ")

    url="https://fr.openfoodfacts.org/cgi/search.pl"

    args = {
            'action': "process",
            'search_terms': context['user_search'],
            # 'nutrition_grades': 'c',
            # 'nutrition_grades': 'd',
            # 'nutrition_grades': 'e',
            'json': 1,
            'page_size': 10,
            }
    # args = {
    #         'action': "process",
    #         'tagtype_0': "categories",
    #         'tag_contains_0': "contains",
    #         'tag_0': category,
    #         'nutrition_grades': grade,
    #         'json': 1,
    #         'page_size': 1000,
    #         }
    response = requests.get(url, params=args)
    products = []

    for product in response.json()["products"]:
        try:
            new_product = {}
            new_product['product_name'] = product['product_name']
            new_product['grade'] = product['nutrition_grades']
            new_product['barcode'] = product['code']
            new_product['categories'] = product['categories_hierarchy'][::-1]
            products.append(new_product)
            # products.append(product['product_name'])
        except KeyError:
            pass

    context['products'] = products

    return render(request, 'openfood/search_on_off.html', context)

def get_substitutes_on_off(request, barcode):
    # rechercher le produit 
    pass


    
def product_substitutes(request, pk):
    # TODO FAIRE UNE FONCTION HORS DE LA VUE dans un 'manager' Cf https://docs.djangoproject.com/en/2.1/topics/db/managers/
    context = Product.objects.get_substitutes(pk)
    # context['product'] = Product.objects.get(pk=pk)
    # categories = context['product'].categories.all()
    # positions = Position.objects.filter(product=context['product'])

    # categories_and_rank = []
    # for category in categories:
    #     categories_and_rank.append(
    #         (category.category_name, category.position_set.get(
    #             category=category, product=context['product']))
    #         )

    # for category, rank in categories_and_rank:
    #     substitutes = Category.objects.filter(
    #         category_name=category).first().products.all().filter(
    #         Q(grade="a") | Q(grade="b")).order_by('?')
    #     if substitutes.count() != 0:
    #         context['substitutes'] = substitutes
    #         break

    # if substitutes.count() == 0:
    #     context['substitutes'] = None


    return render(request, 'openfood/product.html', context)


def ramdom_product(request):
    product_e = Product.objects.filter(grade='e').order_by('?').first()
    context = Product.objects.get_substitutes(product_e.pk)
    return render(request, 'openfood/product.html', context)
    # return HttpResponseRedirect(reverse(product_substitutes, kwargs={'pk': product_e.id}))
