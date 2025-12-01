from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='inventory_list'),
    path('create/', views.item_create, name='item_create'),
    path('<str:pk>/', views.item_detail, name='item_detail'),
    path('<str:pk>/edit/', views.item_edit, name='item_edit'),
    path('<str:pk>/delete/', views.item_delete, name='item_delete'),
]
