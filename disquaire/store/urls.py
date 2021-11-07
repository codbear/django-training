from django.urls import path

from . import views

urlpatterns = [
    path('', views.listing),
    path('albums/<int:album_id>/', views.single),
    path('search/', views.search),
]