from django.urls import path
from . import views

urlpatterns = [
    # blog posts
    path('', views.michi_posts, name='michi_posts'),
    path('add_posts', views.add_posts, name='add_posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/comment/<int:comment_id>/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/star/<int:stars>/', views.set_post_stars, name='set_post_stars'),

    # logins
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
    path('register', views.register, name='register'),
    path('edit_profile', views.edit_profile, name='edit_profile'),

]


