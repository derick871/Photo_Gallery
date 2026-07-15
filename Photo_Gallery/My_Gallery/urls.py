from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.gallery_home, name='gallery_home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('photo/upload/', views.upload_photo, name='upload_photo'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:photo_id>/edit/', views.edit_photo, name='edit_photo'),
    path('photo/<int:photo_id>/delete/', views.delete_photo, name='delete_photo'),
    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),
    path('photo/<int:photo_id>/dislike/', views.dislike_photo, name='dislike_photo'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/password/', views.password_change, name='password_change'),
]