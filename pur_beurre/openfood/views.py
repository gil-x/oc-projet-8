from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Product, Category, Position
from .forms import SearchForm
from django.db.models import Q
import json

def get_products(request):
    """
    This view provides a JSON set of products of all grades but A.
    Used by jQuery autocomplete to suggests registered products.
    """
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('term', '')
        products = Product.objects.filter(
            Q(product_name__icontains = q) &
            Q(grade='e') | Q(grade='d') | Q(grade='c') | Q(grade='b')
            )[:10]
        results = []
        
        print("===\nHello product!\n===")
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
    context['x'] = "ok, je suis là !"
    print("context=", context)
    
    if form.is_valid(): 
        context['search'] = form.cleaned_data['search']
        matching_products = Product.objects.filter(product_name__icontains=context['search'])

        if matching_products:
            context['x'] = "Oh, mais ça marche en plus !"
            context['result'] = matching_products[0]
            # return render(request, 'openfood/index.html', context)
            return HttpResponseRedirect(reverse(product_substitutes, kwargs={'pk': matching_products[0].pk}))
            return render(request, 'openfood/product.html', pk=matching_products[0].id)

            pass
            # search substitute
            # return substitute_page(id prduct)
        else:
            context['x'] = "Hum, y a un os..."
            return render(request, 'openfood/index.html', context)
            pass
            # req1 : search the product on openfood
            # req2 : search substutes on openfood
            # OR 
            # req1 : search the product on openfood
            # get his best category
            # req2: download subsitutes of this categories
            # redo the operation with the new product id

    else:
        return render(request, 'openfood/index.html', context)

    
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
    # context['product_e_cats_and_rank'] = categories_and_rank

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
    context = {}

    product_e = Product.objects.filter(grade='e').order_by('?').first()
    context['product_e'] = product_e

    categories = product_e.categories.all()
    positions = Position.objects.filter(product=product_e)

    for p in positions:
        print(p.rank, p.category)

    categories_and_rank = []
    for category in categories:
        categories_and_rank.append(
            (category.category_name,
            category.position_set.get(category=category, product=product_e),)
            )
    context['product_e_cats_and_rank'] = categories_and_rank

    for category, rank in categories_and_rank:
        # substitutes = Category.objects.filter(category_name=category).first().products.all().filter(grade="b").order_by('?')
        substitutes = Category.objects.filter(
            category_name=category).first().products.all().filter(
            Q(grade="a") | Q(grade="b")).order_by('?')
        if substitutes.count() != 0:
            context['substitutes'] = substitutes
            break

    if substitutes.count() == 0:
        context['substitutes'] = "rien" # TODO The template should returns Error...

    return HttpResponseRedirect(reverse(product_substitutes, kwargs={'pk': 123}))
    return render(request, 'openfood/sample.html', context)



