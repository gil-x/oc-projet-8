from django.shortcuts import render
from .models import Product

def search_product(request):
    pass

def ramdom_product(request):
    context = {}

    product_e = Product.objects.filter(grade='e').order_by('?').first()
    context['product_e'] = product_e

    categories = product_e.categories.all()
    categories_and_rank = []
    for category in categories:
        categories_and_rank.append(
            (category.category_name,
            category.position_set.get(category=category, product=product_e),)
            )
    context['product_e_cats_and_rank'] = categories_and_rank


    # Find subsitute:
    # get all products in more precise category
    # if none : get all products in the second more precise categorie
    # if there are products, HOW to choose ? => compare other cats or need new fiels like keywords ?

    # After User can say if result is nice or not.

    return render(request, 'openfood/sample.html', context)