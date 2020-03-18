from django.urls import path

from . import views


app_name = 'ui'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('restaurant/create/', views.CreateRestaurantView.as_view(), name='restaurant_create'),
]
