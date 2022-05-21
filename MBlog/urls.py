from django.urls import path
from . import views

urlpatterns = [
    # blog posts
    path('', views.michi_posts, name='michi_posts'),
]


