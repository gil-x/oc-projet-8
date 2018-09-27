from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Category, Position
from .forms import SearchForm
from django.db.models import Q
import json

def get_products(request):
    if request.is_ajax() or request.method == 'GET':
        q = request.GET.get('term', '')
        products = Product.objects.filter(product_name__icontains = q )[:5]
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
        context['result'] = Product.objects.filter(product_name__icontains=context['search'], grade="e")[0]

        # product_to_substitute = context['result']
        # good_substitute = Product.objects.filter(product_name__icontains=context['search'], grade="e")

    return render(request, 'openfood/index.html', context)


def ramdom_product(request):
    context = {}

    product_e = Product.objects.filter(grade='e').order_by('?').first()
    context['product_e'] = product_e

    categories = product_e.categories.all()
    positions = Position.objects.filter(product=product_e)
    print("\n====\n", positions)
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

    return render(request, 'openfood/sample.html', context)



