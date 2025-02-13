from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entrypage, name="entrypage"),
    path("newpage/", views.newpage, name="newpage"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random/", views.random_page, name="random"), 
    
    
    path("error/", views.errorpage, name="errorpage"), 
    
    path("search/", views.search, name="search"),
]
