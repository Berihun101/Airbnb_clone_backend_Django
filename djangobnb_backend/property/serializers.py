from rest_framework import serializers
from .models import Property, Reservation
from useraccount.serializers import UserDetailSerializer

class PropertyScerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url', 
        )

class PropertyDetailSerializer(serializers.ModelSerializer):
    landlord = UserDetailSerializer(read_only=True)
    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'price_per_night',
            'image_url',
            'description',
            'bedrooms',
            'bathrooms',
            'guests',
            'country',
            'country_code',
            'landlord',
            'category',
            'created_at',
        )


class ReservationsListSerializer(serializers.ModelSerializer):
    property = PropertyScerializer(read_only=True, many=False)
    class Meta:
        model = Reservation
        fields = (
            'id',
            'property',
            'start_date',
            'end_date',
            'number_of_nights',
            'total_price',
            'guest',
            'created_at',
        )