from django.shortcuts import render, redirect, HttpResponse

# Create your views here.


def michi_posts(request):
    return render(request, 'michi_posts.html')
