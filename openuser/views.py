from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from openfood.models import Product
from .forms import CreateUser, LoginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def registration(request):
    context = {}
    if "currentsearch" in request.session:
        context["currentsearch"] = request.session["currentsearch"]
    else:
        context["currentsearch"] = "logout"
    context["form"] = CreateUser(request.POST or None)
    if context["form"].is_valid():
        username = context["form"].cleaned_data['username']
        password = context["form"].cleaned_data['password']
        email = context["form"].cleaned_data['email']
        new_user = User.objects.create_user(username)
        new_user.set_password(password)
        new_user.email = email
        new_user.save()
        new_profile = Profile()
        new_profile.user = new_user
        new_profile.save()
        if authenticate(username=new_user.username, password=password):
            login(request, new_user)
            if "random" in context["currentsearch"]:
                """
                If coming from random product page,
                then redirect to the same product as standard substitute page.
                """
                return HttpResponseRedirect(
                    reverse_lazy(
                        'product_substitutes',
                        kwargs={'pk': context["currentsearch"].replace("random_", "")}
                        ),
                    )
            else:
                return HttpResponseRedirect(reverse_lazy('search_product'))
    return render(request, 'openuser/registration.html', context)

def log_in(request):
    context = {}
    if "currentsearch" in request.session:
        context["currentsearch"] = request.session["currentsearch"]
    else:
        context["currentsearch"] = "logout"
    context["form"] = form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if request.method == 'GET' and 'next' in request.GET:
                return redirect(request.GET['next'])
            elif "random" in context["currentsearch"]:
                """
                If coming from random product page,
                then redirect to the same product as standard substitute page.
                """
                return HttpResponseRedirect(
                    reverse_lazy(
                        'product_substitutes',
                        kwargs={'pk': context["currentsearch"].replace("random_", "")}
                        ),
                    )
            return HttpResponseRedirect(reverse_lazy('search_product'))
    return render(request, 'openuser/connexion.html', context)

@login_required
def user_account(request):
    context = {}
    context["favorites_number"] = len(request.user.profile.products.all())
    return render(request, 'openuser/account.html', context)

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('search_product'))

@login_required
def user_favorites(request):
    favorites = request.user.profile.products.all()
    paginator = Paginator(favorites, 6)
    page = request.GET.get('page')
    try:
        favorites_p = paginator.page(page)
    except PageNotAnInteger:
        favorites_p = paginator.page(1)
    except EmptyPage:
        favorites_p = paginator.page(paginator.num_pages)

    return render(request, 'favorites_p.html', {'favorites_p': favorites_p})

    # return render(request, 'openuser/favorites.html', {'favorites': favorites})

@login_required
def add_to_favorites(request, pk):
    context = {}
    product_to_add = Product.objects.all().filter(pk=pk).first()
    context['product'] = product_to_add
    if product_to_add:
        context['response'] = "Y a un produit."
        request.user.profile.products.add(product_to_add)
    else:
        context['response'] = "Y a PAS d'produit !"
    return render(request, 'openuser/favorites.html', context)

@login_required
def remove_from_favorites(request, pk):
    context = {}
    product_to_remove = request.user.profile.products.filter(pk=pk).first()
    request.user.profile.products.remove(product_to_remove)
    context['to_delete'] = product_to_remove
    return render(request, 'openuser/favorites.html', context)