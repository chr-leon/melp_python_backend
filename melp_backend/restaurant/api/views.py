from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
import csv
from django.views.decorators.csrf import csrf_exempt




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
                restaurantExists=allRestaurants.get(id=row['id'])
                serializedRestaurant=RestaurantSerializer(instance=restaurantExists,data=row)
                if serializedRestaurant.is_valid():
                    serializedRestaurant.save()                    
                else:
                    print(serializedRestaurant.errors)
            return JsonResponse({'message': 'Archivo CSV procesado exitosamente'}, status=200)

    
# @csrf_exempt
# def uploadCsv(request):
#     if request.method == 'POST' and request.FILES['csv_file']:
#         csv_file = request.FILES['csv_file']
#         # Aquí puedes procesar el archivo CSV según tus necesidades
#         # Por ejemplo, puedes leerlo línea por línea y hacer algo con los datos
#         decoded_file = csv_file.read().decode('utf-8').splitlines()
#         reader = csv.DictReader(decoded_file)
#         validRestaurants=[]
#         for row in reader:
#             serializedRestaurant=RestaurantSerializer(data=row)
#             if serializedRestaurant.is_valid():
#                 serializedRestaurant.save()
#             else:
#                 print(serializedRestaurant.errors)
#         return JsonResponse({'message': 'Archivo CSV procesado exitosamente'}, status=200)
