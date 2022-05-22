from django.urls import path
from . import views

urlpatterns = [
    # blog posts
    path('', views.michi_posts, name='michi_posts'),
    path('add_posts', views.add_posts, name='add_posts'),

    # logins
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),

]


