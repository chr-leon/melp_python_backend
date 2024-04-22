from rest_framework import serializers
from restaurant.models import Restaurant
from django.contrib.gis.db import models
import uuid

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "rating", "name", "site", "email", "phone", "street", "city", "state", "coordinates"]

        # extra_kwargs = {
        #     'role_name':{'required':True}
        # }



class CreateRestaurantSerializer(serializers.Serializer):
    
        rating = serializers.FloatField()
        name = serializers.CharField(max_length=100)
        site = serializers.CharField(max_length=1000)
        email = serializers.EmailField(max_length=254)
        phone = serializers.CharField(max_length=20)
        street = serializers.CharField(max_length=200)
        city = serializers.CharField(max_length=100)
        state = serializers.CharField(max_length=100)
        latitude = serializers.FloatField()
        longitude = serializers.FloatField()
        
        def validate(self, data):
            errors = {}

            if data.get('latitude') == None:
                errors['latitude'] = "Latitude is required"

            if data.get('longitude') == None:
                errors['longitude'] = "Longitude is required"

            if data.get('name') == None:
                errors['name'] = "Name is required"

            if data.get('rating') == None:
                errors['rating'] = "Rating is required"

            if data.get('site') == None:
                errors['site'] = "Site is required"

            if data.get('email') == None:
                errors['email'] = "Email is required"

            if data.get('phone') == None:
                errors['phone'] = "Phone is required"

            if data.get('street') == None:
                errors['street'] = "Street is required"

            if data.get('city') == None:
                errors['city'] = "City is required"

            if data.get('state') == None:
                errors['state'] = "State is required"

            if bool(errors.keys()):
                print(errors)
                print(data)
                raise serializers.ValidationError(errors)

            return data
    