#from django.db import models
from django.contrib.gis.db import models
import uuid

class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    rating = models.FloatField()
    name = models.CharField(max_length=100)
    site = models.CharField(max_length=1000)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    coordinates = models.PointField()
    class Meta:
        db_table="restaurant"