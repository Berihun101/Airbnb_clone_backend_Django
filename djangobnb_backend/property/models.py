from django.db import models
import uuid
from django.conf import settings
from useraccount.models import User


# Create your models here.

class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    landlord = models.ForeignKey(User, related_name="properties", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    guests = models.IntegerField()
    image = models.ImageField(upload_to="uploads/properties")
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    category = models.CharField(max_length=100)
    favorited = models.ManyToManyField(User, related_name="favorites", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#change the name of the table in the database
    
    def __str__(self):
        return self.title
    
    def image_url(self):
        return f'{settings.MEDIA_URL}{self.image}'
    
class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, related_name="reservations", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_nights = models.IntegerField()
    guest = models.IntegerField()
    total_price = models.FloatField()
    created_by = models.ForeignKey(User, related_name="reservations", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.property.title} - {self.created_by.name}'
