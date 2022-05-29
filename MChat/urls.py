from django.urls import path
from . import views

urlpatterns = [
    # roofs
    path('', views.create_roof, name='create_roof'),
    path('<str:roof_id>/', views.roof, name='roof'),
    path('<str:roof_id>/update_name', views.set_roof_name, name='set_roof_name'),
]


