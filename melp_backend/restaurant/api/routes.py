from django.urls import path
from restaurant.api.views import RestaurantViewSet;

app_name="restaurant"

urlpatterns = [
    path('', RestaurantViewSet.as_view({ 'post':'post' }),name='postRestaurant'),
    path('<str:pk>/', RestaurantViewSet.as_view({ 'get':'get' }),name='getRestaurant'),
    path('<str:pk>/', RestaurantViewSet.as_view({ 'put':'put' }),name='putRestaurant'),
    path('<str:pk>/', RestaurantViewSet.as_view({ 'delete':'delete' }),name='deleteRestaurant'),
    path('import', RestaurantViewSet.as_view({ 'post':'importCsv' })),
    path('statistics', RestaurantViewSet.as_view({ 'get':'getStatistics' }, name ="statistics"))
]