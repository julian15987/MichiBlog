from django.urls import path
from . import views

urlpatterns = [
    # blog posts
    path('', views.michi_posts, name='michi_posts'),

    # logins
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),

]


