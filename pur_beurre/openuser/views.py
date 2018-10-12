from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
from openfood.models import Product
from .forms import CreateUser, LoginForm

def registration(request):
    form = CreateUser(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        new_user = User.objects.create_user(username)
        new_user.set_password(password)
        new_user.email = email
        new_user.save()
        new_profile = Profile()
        new_profile.user = new_user
        new_profile.save()
        if authenticate(username=new_user.username, password=password):
            login(request, new_user)
    return render(request, 'openuser/registration.html', {'form': form})

def log_in(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET['next'])
    return render(request, 'openuser/connexion.html', {'form': form})

@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('log_in'))

@login_required
def user_favorites(request):
    favorites = request.user.profile.products.all()
    return render(request, 'openuser/favorites.html', {'favorites': favorites})

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