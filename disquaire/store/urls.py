from django.urls import path

from . import views

app_name = 'store'
urlpatterns = [
    path('', views.listing, name='listing'),
    path('albums/<int:album_id>/', views.single, name='single'),
    path('search/', views.search, name='search'),
]