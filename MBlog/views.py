from django.shortcuts import render, redirect, HttpResponse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .models import MichiPost


# Blog
def michi_posts(request):
    posts = MichiPost.objects.filter(erased=False)
    posts = posts.order_by('-created_at')

    return render(request, 'index.html', {'posts': posts})


# Logins
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
        else:
            messages.error(request, "Invalid Credentials")
            return redirect("/login")
        return redirect("/")

    return render(request, 'login.html')


def logout_request(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')
