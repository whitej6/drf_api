from django.urls import path

from . import views


app_name = 'ui'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('restaurant/create/', views.CreateRestaurantView.as_view(), name='restaurant_create'),
]
