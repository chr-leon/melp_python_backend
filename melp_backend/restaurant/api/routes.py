from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from restaurant.api.views import RestaurantViewSet;

app_name="restaurant"

urlpatterns = [
    path('', RestaurantViewSet.as_view({ 'post':'post' }),name='createRestaurant'),
    path('<str:pk>/', RestaurantViewSet.as_view({ 'get':'get' }),name='getRestaurant'),
    path('<str:pk>/', RestaurantViewSet.as_view({ 'put':'put' }),name='updateRestaurant'),
    path('<str:pk>/', RestaurantViewSet.as_view({ 'delete':'delete' }),name='deleteRestaurant'),
    path('import/', RestaurantViewSet.as_view({ 'post':'importCsv' }))
]