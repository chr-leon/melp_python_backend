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
    
        rating = models.FloatField()
        name = models.CharField(max_length=100)
        site = models.CharField(max_length=1000)
        email = models.EmailField(max_length=254)
        phone = models.CharField(max_length=20)
        street = models.CharField(max_length=200)
        city = models.CharField(max_length=100)
        state = models.CharField(max_length=100)
        coordinates = models.PointField()
        
        def validate(self, data):
            print('executing validator...')
            return data
        # if  not data.get('new_password') ==  data.get('new_password_confirmation'):
        #     raise serializers.ValidationError("La nueva contraseña y su confirmación deben ser iguales")
        # if len(data.get('new_password')) < 8:
        #     raise serializers.ValidationError("Las nuevas contraseñas deben ser de al menos 9 caracteres")
        # validCurrentPassword=check_password(data.get('current_password'),self.context.get("encrypted_password"))
        # if not validCurrentPassword:
        #     raise serializers.ValidationError("Contraseña actual incorrecta")
        # return data