from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView  
import csv
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point



from restaurant.models import Restaurant
from restaurant.api.serializers import RestaurantSerializer,CreateRestaurantSerializer
from django.shortcuts import get_object_or_404,get_list_or_404


class RestaurantViewSet(viewsets.ViewSet):
    
    def get(self,request,pk):
        queryset = Restaurant.objects.all()
        restaurant = get_object_or_404(queryset, pk=pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        queryset = Restaurant.objects.all()
        restaurant = get_object_or_404(queryset, pk=pk)
        serializer = CreateRestaurantSerializer(restaurant,data=request.data)
        if serializer.is_valid():
            latitude = float(request.data.get('latitude'))
            longitude = float(request.data.get('longitude'))
            point = Point(longitude, latitude, srid=4326)  # SRID 4326 es WGS 84
            dataToSave = {
                'rating':request.data.get('rating'),
                'name':request.data.get('name'),
                'site':request.data.get('site'),
                'email':request.data.get('email'),
                'phone':request.data.get('phone'),
                'street':request.data.get('street'),
                'city':request.data.get('city'),
                'state':request.data.get('state'),
                'coordinates':point
            }
            restauratSerializer = RestaurantSerializer(instance=restaurant,data=dataToSave);
            if(restauratSerializer.is_valid()):
                restauratSerializer.save()
                return JsonResponse(restauratSerializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)
    
    def delete(self,request,pk):
        queryset = Restaurant.objects.all()
        restaurant = get_object_or_404(queryset, pk=pk)
        restaurant.delete()
        return JsonResponse({'message':'Restaurante eliminado exitosamente'},status=200)
    
    def post(self,request):

        
        serializer = CreateRestaurantSerializer(data=request.data)
        if serializer.is_valid():
            latitude = float(request.data.get('latitude'))
            longitude = float(request.data.get('longitude'))
            point = Point(longitude, latitude, srid=4326)  # SRID 4326 es WGS 84
            dataToSave = {
                'rating':request.data.get('rating'),
                'name':request.data.get('name'),
                'site':request.data.get('site'),
                'email':request.data.get('email'),
                'phone':request.data.get('phone'),
                'street':request.data.get('street'),
                'city':request.data.get('city'),
                'state':request.data.get('state'),
                'coordinates':point
            }
            print('-----------------data to save-----------------')
            print(dataToSave)
            restauratSerializer = RestaurantSerializer(data=dataToSave);
            if(restauratSerializer.is_valid()):
                restauratSerializer.save()
                return JsonResponse(restauratSerializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)
    
    def getStatistics(self,request):
        params = request.query_params

        if(params.get('latitude') is not None and params.get('longitude') is not None and params.get('radius') is not None):
            latitude = float(params.get('latitude'))
            longitude = float(params.get('longitude'))
            radius = float(params.get('radius'))
            query_set = restaurants_within_radius(latitude,longitude,radius)
            restaurants =  get_list_or_404(query_set)
            serializedRestaurants = RestaurantSerializer(restaurants,many=True)
            return JsonResponse(serializedRestaurants.data, safe=False,status=201)
        else:
            query_set = Restaurant.objects.all()
            restaurants =  get_list_or_404(query_set)
            serializedRestaurants = RestaurantSerializer(restaurants,many=True)
            return JsonResponse(serializedRestaurants.data,safe=False,status=201)
    
    @csrf_exempt
    def importCsv(self,request):
        if request.method == 'POST' and request.FILES['csv_file']:
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                allRestaurants=Restaurant.objects.all()
                restaurantExists=allRestaurants.filter(id=row['id']).first()
                serializedRestaurant=RestaurantSerializer(instance=restaurantExists,data=row)
                if serializedRestaurant.is_valid():
                    if(restaurantExists is None):
                        serializedRestaurant.save(id=row['id'])                    
                    else:
                        serializedRestaurant.save(instance=restaurantExists)                    
                    
                else:
                    print(serializedRestaurant.errors)
            return JsonResponse({'message': 'Archivo CSV procesado exitosamente'}, status=200)

def restaurants_within_radius(latitude, longitude, radius_in_meters):
    # Crear un objeto Point para las coordenadas de partida
    point = Point(longitude, latitude, srid=4326)  # SRID 4326 es WGS 84

    # Realizar la consulta para encontrar ubicaciones dentro del radio dado
    restaurants = Restaurant.objects.filter(coordinates__distance_lte=(point, radius_in_meters))

    return restaurants