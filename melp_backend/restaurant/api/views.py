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
from restaurant.api.serializers import RestaurantSerializer
from django.shortcuts import get_object_or_404


class RestaurantViewSet(viewsets.ViewSet):
    
    def get(self,request,pk):
        queryset = Restaurant.objects.all()
        restaurant = get_object_or_404(queryset, pk=pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        queryset = Restaurant.objects.all()
        restaurant = get_object_or_404(queryset, pk=pk)
        serializer = RestaurantSerializer(restaurant,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=200)
        return JsonResponse(serializer.errors,status=400)
    
    def delete(self,request,pk):
        queryset = Restaurant.objects.all()
        restaurant = get_object_or_404(queryset, pk=pk)
        restaurant.delete()
        return JsonResponse({'message':'Restaurante eliminado exitosamente'},status=200)
    
    def post(self,request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)
    
    @csrf_exempt
    def importCsv(self,request):
        if request.method == 'POST' and request.FILES['csv_file']:
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            validRestaurants=[]
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


class RestaurantsListView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filterset_fields = ['latitude', 'longitude']
    search_fields=('name','model','asset_type__name')
    def set_queryset(self):
        params = self.request.query_params
        point = Point(params.longitude, params.latitude, srid=4326)  # SRID 4326 es WGS 84
        restaurants = Restaurant.objects.filter(coordinates__distance_lte=(point, params.radius))
        return restaurants