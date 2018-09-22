from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profile
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
            return HttpResponseRedirect(reverse_lazy('search_product'))

    return render(request, 'openuser/connexion.html', {'form': form})


@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('log_in'))


def favorites(request):
    favorites = request.user.profile.products.all()
    user = request
    return render(request, 'openuser/favorites.html', {'favorites': favorites, 'test': user})