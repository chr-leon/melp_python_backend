from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from restaurant.api.views import RestaurantViewSet;

app_name="restaurant"

urlpatterns = [
    path('<str:pk>', RestaurantViewSet.as_view({ 'get':'retrieve' })),
    path('import/', RestaurantViewSet.as_view({ 'post':'importCsv' }))
]