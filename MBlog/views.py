from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .models import MichiPost, MichiProfile
from .forms import MichiPostForm


# Blog
def michi_posts(request):
    posts = MichiPost.objects.filter(erased=False)
    posts = posts.order_by('-created_at')

    return render(request, 'index.html', {'posts': posts})


@login_required(login_url='/login')
def add_posts(request):
    if request.method == "POST":
        form = MichiPostForm(data=request.POST, files=request.FILES)
        michi_author = MichiProfile.objects.get(user=request.user.id)

        if not michi_author:
            messages.error(request, "El perfil del michi tiene que estar creado para poder crear un post")
            return redirect("/")

        if form.is_valid():
            MichiPost = form.save(commit=False)
            MichiPost.michi_author = michi_author
            MichiPost.save()
            obj = form.instance
            messages.success(request, 'El MichiPost se agrego al MichiBlog !')
            return redirect("/")
    else:
        form = MichiPostForm()
    return render(request, "add_post.html", {'form': form})

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
