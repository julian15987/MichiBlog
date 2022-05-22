from django.urls import path
from . import views

urlpatterns = [
    # blog posts
    path('', views.michi_posts, name='michi_posts'),
    path('add_posts', views.add_posts, name='add_posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),

    # logins
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
]


