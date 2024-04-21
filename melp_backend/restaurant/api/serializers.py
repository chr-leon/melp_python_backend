from rest_framework import serializers
from restaurant.models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "rating", "name", "site", "email", "phone", "street", "city", "state", "latitude", "longitude"]

        # extra_kwargs = {
        #     'role_name':{'required':True}
        # }
