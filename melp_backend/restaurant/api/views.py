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
    
    def retrieve(self,request,pk):
        queryset = Restaurant.objects.all()
        restaurant = get_object_or_404(queryset, pk=pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
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
