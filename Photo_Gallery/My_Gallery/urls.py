from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= "index"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile, name= "profile"),
    path('photo_details' views.photo_details, name= "photo_details"),

]