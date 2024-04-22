from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
import csv
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis.geos import Point
from django.db.models import Count, Avg, StdDev




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
        serializer = CreateRestaurantSerializer(data=request.data)
        if serializer.is_valid():
            latitude = float(request.data.pop('latitude'))
            longitude = float(request.data.pop('longitude'))
            point = Point(longitude, latitude, srid=4326)  # SRID 4326 es WGS 84
            request.data['coordinates']=point
            restauratSerializer = RestaurantSerializer(instance=restaurant,data=request.data);
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

        print(request.data)
        serializer = CreateRestaurantSerializer(data=request.data)
        if serializer.is_valid():
            latitude = float(request.data.pop('latitude'))
            longitude = float(request.data.pop('longitude'))
            point = Point(longitude, latitude, srid=4326)  # SRID 4326 es WGS 84
            request.data['coordinates']=point
            restauratSerializer = RestaurantSerializer(data=request.data);
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
            restaurants_inside_circle = restaurants_within_radius(latitude,longitude,radius)
            count = restaurants_inside_circle.count()
            avg_rating = restaurants_inside_circle.aggregate(avg_rating=Avg('rating'))['avg_rating']
            std_rating = restaurants_inside_circle.aggregate(std_rating=StdDev('rating'))['std_rating']

            data = {
                'count': count,
                'avg': avg_rating,
                'std': std_rating
            }
            return JsonResponse(data,status=200)
        else:
            return JsonResponse({
                'count':0,
                'avg':0,
                'std':0
            },status=200)
    
    @csrf_exempt
    def importCsv(self,request):
        if request.method == 'POST' and request.FILES['csv_file']:
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:

                allRestaurants=Restaurant.objects.all()
                restaurantExists=allRestaurants.filter(id=row['id']).first()
                isValidInput = CreateRestaurantSerializer(data=row)
                if isValidInput.is_valid():
                    latitude = float(row.pop('latitude'))
                    longitude = float(row.pop('longitude'))
                    point = Point(longitude, latitude, srid=4326)  # SRID 4326 es WGS 84
                    row['coordinates']=point
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
    
    point = Point(longitude, latitude, srid=4326)  # SRID 4326 es WGS 84

    restaurants = Restaurant.objects.filter(coordinates__distance_lte=(point, radius_in_meters))

    return restaurants