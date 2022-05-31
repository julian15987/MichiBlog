import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .models import MichiPost, MichiProfile, MichiComments, MichiStars, PostCategories
from .forms import MichiPostForm, MichiProfileForm, PostCategoriesForm
import MBlog.constants as constants


# Blog
def michi_posts(request):
    posts = MichiPost.objects.filter(erased=False)
    posts = posts.order_by('-created_at')
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, constants.POST_PER_PAGE)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/index.html', {'posts': posts, 'favourites': False})


@login_required(login_url='/login')
def fav_michi_posts(request):
    star_posts = MichiStars.objects.filter(michi_author=request.user.michiprofile, stars__gte=constants.STARS_FOR_FAVOURITE).all()
    star_posts = star_posts.order_by('-created_at')
    posts = []
    for post in star_posts:
        posts.append(post.michi_post)
    return render(request, 'blog/index.html', {'posts': posts, 'favourites': True})


def post_detail(request, post_id):
    try:
        post = MichiPost.objects.get(id=post_id)
    except MichiPost.DoesNotExist as e:
        return page_not_found(request)
    try:
        stars = MichiStars.objects.filter(michi_post=post, michi_author=request.user.michiprofile).first()
    except AttributeError as e:
        stars = None

    count_stars = MichiStars.objects.filter(michi_post=post).aggregate(Sum('stars'))

    return render(request, 'blog/post_detail.html', {'post': post, 'stars': stars, 'count_stars': count_stars['stars__sum'], 'favorite': constants.STARS_FOR_FAVOURITE})


@login_required(login_url='/login')
def set_post_stars(request, post_id, stars):
    try:
        post = MichiPost.objects.get(id=post_id)
        michi_stars = MichiStars.objects.filter(michi_post=post, michi_author=request.user.michiprofile).first()
    except MichiPost.DoesNotExist as e:
        return page_not_found(request)

    if michi_stars:
        michi_stars.stars = int(stars)
    else:
        michi_stars = MichiStars(michi_post=post, michi_author=request.user.michiprofile, stars=int(stars))
    michi_stars.save()

    return redirect("/post/"+str(post_id))


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
            messages.success(request, 'El MichiPost se agrego al MichiBlog !')
            return redirect("/")
    else:
        form = MichiPostForm()
    return render(request, "blog/add_post.html", {'form': form})


@login_required(login_url='/login')
def add_comment(request, post_id, comment_id=None):
    if request.method == "POST":
        if comment_id is not None:
            parent_comment = MichiComments.objects.get(id=comment_id)
        else:
            parent_comment = None

        comment = request.POST['comment']

        if comment == "":
            messages.error(request, "El comentario no puede estar vacio")
            return redirect("/post/" + str(post_id) + '/')

        michi_post = MichiPost.objects.get(id=post_id)
        michi_comment = MichiComments(content=comment,
                                      michi_post=michi_post,
                                      parent_comment=parent_comment,
                                      michi_author=request.user.michiprofile)
        michi_comment.save()

    return redirect("/post/" + str(post_id) + '/')


@login_required(login_url='/login')
def delete_comment(request, comment_id):
    if request.method == "POST":
        comment = MichiComments.objects.get(id=comment_id)
        if comment_id is None:
            messages.error(request, "El comentario no puede estar vacio")
            return redirect("/post/" + str(comment.michi_post.id) + '/')
        comment.delete()
        return redirect("/post/" + str(comment.michi_post.id) + '/')


@login_required(login_url='/login')
def delete_post(request, post_id):
    if request.method == "POST":
        post = MichiPost.objects.get(id=post_id)
        if post_id is None:
            messages.error(request, "El post no puede estar vacio")
            return redirect("/post/" + str(post_id) + '/')
        post.delete()
    return redirect("/")


# Categories
@login_required(login_url='/login')
def get_categories(request):
    categories = PostCategories.objects.all()
    return render(request, 'blog/categories.html', {'categories': categories})


@login_required(login_url='/login')
def add_category(request):
    if request.method == "POST":
        form = PostCategoriesForm(data=request.POST)

        if form.is_valid():
            post_category = form.save(commit=True)
            messages.success(request, 'La categoria se agrego al MichiBlog !')
            return redirect("/categories")
    else:
        form = PostCategoriesForm()
    return render(request, "blog/add_category.html", {'form': form})


@login_required(login_url='/login')
def delete_category(request, category_id):
    if request.method == "POST":
        category = PostCategories.objects.get(id=category_id)
        if category_id is None:
            messages.error(request, "La categoria no puede estar vacio")
            return redirect("/categories")
        category.delete()
        messages.success(request, "Se elimina la categoria")
    return redirect("/categories")


@login_required(login_url='/login')
def edit_category(request, category_id):
    if request.method == "POST":
        category = PostCategories.objects.get(id=category_id)
        form = PostCategoriesForm(data=request.POST, instance=category)

        if form.is_valid():
            post_category = form.save(commit=True)
            messages.success(request, 'Se modifico la categoria')
            return redirect("/categories")
    else:
        category = PostCategories.objects.get(id=category_id)
        form = PostCategoriesForm(instance=category)
    return render(request, "blog/edit_category.html", {'form': form, 'category_id':category_id})


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


def view_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        profile = MichiProfile.objects.get(user=user)
        posts = MichiPost.objects.filter(michi_author=profile).order_by('-created_at')[:constants.POST_PER_PROFILE]
        comments = MichiComments.objects.filter(michi_author=profile).order_by('-created_at')[:constants.COMMENTS_PER_PROFILE]
    except User.DoesNotExist as e:
        return page_not_found(request)

    return render(request, 'blog/profile.html', {'profile': profile, 'posts': posts, 'comments': comments})


def michi_ping(request):
    return HttpResponse("pong")


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
            return redirect("/view_profile/" + str(request.user.id))
    else:
        form = MichiProfileForm()
        form.fields['nickname'].initial = request.user.michiprofile.nickname
        form.fields['hair_color'].initial = request.user.michiprofile.hair_color
        form.fields['eye_color'].initial = request.user.michiprofile.eye_color
        form.fields['birthday'].initial = request.user.michiprofile.birthday
        form.fields['erased'].initial = request.user.michiprofile.erased

    return render(request, "blog/edit_profile.html", {'form': form})


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        nick = request.POST['nick']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')

        try:
            user = User.objects.create_user(username, email, password1)
            user.save()
            michi_profile = MichiProfile(user=user, nickname=nick)
            michi_profile.save()
            return render(request, 'login.html')
        except Exception as e:
            messages.error(request, "Username or email already exists.")
            return redirect('/register')
    return render(request, "register.html")


# Errors

def page_not_found(request):
    return render(request, 'errors/404.html', status=404)


# About

def about(request):
    return render(request, 'about.html')
