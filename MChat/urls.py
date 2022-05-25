from django.urls import path
from . import views

urlpatterns = [
    # roofs
    path('', views.create_roof, name='create_roof'),
]


