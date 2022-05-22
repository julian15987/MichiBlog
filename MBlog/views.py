import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.utils import IntegrityError

from .models import MichiPost, MichiProfile
from .forms import MichiPostForm, MichiProfileForm


# Blog
def michi_posts(request):
    posts = MichiPost.objects.filter(erased=False)
    posts = posts.order_by('-created_at')

    return render(request, 'index.html', {'posts': posts})


def post_detail(request, post_id):
    post = MichiPost.objects.get(id=post_id)
    return render(request, 'post_detail.html', {'post': post})


@login_required(login_url='/login')
def add_posts(request):
    if request.method == "POST":
        form = MichiPostForm(data=request.POST, files=request.FILES)
        michi_author = MichiProfile.objects.get(user=request.user.id)

        if not michi_author:
            messages.error(request, "El perfil del michi tiene que estar creado para poder crear un post")
            return redirect("/")

        if form.is_valid():
            michi_post = form.save(commit=False)
            michi_post.michi_author = michi_author
            michi_post.save()
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


@login_required(login_url='/login')
def logout_request(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')


@login_required(login_url='/login')
def edit_profile(request):
    img = request.user.michiprofile.profile_picture
    if request.method == "POST":
        form = MichiProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            michi_profile = form.save(commit=False)
            michi_profile.id = request.user.michiprofile.id
            if not request.user.michiprofile:
                michi_profile.created_at = datetime.datetime.now()
            else:
                michi_profile.created_at = request.user.michiprofile.created_at
            michi_profile.user = request.user
            if not michi_profile.profile_picture:
                michi_profile.profile_picture = img
            michi_profile.save()
            messages.success(request, "Successfully updated profile")
            return redirect("/")
    else:
        form = MichiProfileForm()
        form.fields['nickname'].initial = request.user.michiprofile.nickname
        form.fields['hair_color'].initial = request.user.michiprofile.hair_color
        form.fields['eye_color'].initial = request.user.michiprofile.eye_color
        form.fields['birthday'].initial = request.user.michiprofile.birthday
        form.fields['erased'].initial = request.user.michiprofile.erased

    return render(request, "edit_profile.html", {'form': form})


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')

        user = User.objects.create_user(username, email, password1)
        user.save()
        michi_profile = MichiProfile(user=user)
        michi_profile.save()
        return render(request, 'login.html')
    return render(request, "register.html")
