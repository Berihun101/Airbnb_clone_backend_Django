from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes # type: ignore
from useraccount.models import User
from rest_framework_simplejwt.tokens import AccessToken
from .models import Property, Reservation
from .serializers import PropertyScerializer, PropertyDetailSerializer, ReservationsListSerializer
from .forms import PropertyForm

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def properties_list(request):
    # Auth
    try:
        token = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[1].strip()
        token = AccessToken(token)
        user_id = token.payload['user_id']
        user = User.objects.get(id=user_id)
    except Exception as e:
        print(f"Auth error: {e}")  # Log the error for debugging
        user = None

    

    favorites = []
    properties = Property.objects.all()

    # Filter by landlord
    is_favorite = request.GET.get('is_favorites', '')
    landlord_id = request.GET.get('landlordId', '')
    if landlord_id:
        properties = properties.filter(landlord_id=landlord_id)

    # Filter by favorites
    if is_favorite:
        properties = properties.filter(favorited__in=[user])

    if user:
        for property in properties:
            if user in property.favorited.all():
                favorites.append(property.id)
    

    serializer = PropertyScerializer(properties, many=True)
    return JsonResponse({
        'data': serializer.data,
        'favorites': favorites
    })




@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def property_reservation(request, id):
    try:
        property = Property.objects.get(id=id)
        reservations = property.reservations.all()
        serializer = ReservationsListSerializer(reservations, many=True)
        return JsonResponse({
            'data': serializer.data
            
        }, safe=False)
    except Property.DoesNotExist:
        return JsonResponse({
            'errors': 'Property not found'
        }, status=404)




@api_view(['POST', 'FILES'])
def create_property(request):
    form = PropertyForm(request.POST, request.FILES)
    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()
        return JsonResponse({
            'success': 'Property created successfully'
        })
    return JsonResponse({
        'errors': form.errors.as_json()
    }, status=400)




@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def property_detail(request, id):
    try:
        property = Property.objects.get(id=id)
    except Property.DoesNotExist:
        return JsonResponse({
            'errors': 'Property not found'
        }, status=404)
    serializer = PropertyDetailSerializer(property, many=False)
    return JsonResponse(serializer.data)




@api_view(['POST'])

def book_property(request, id):
    try:
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_night= request.POST.get('number_of_night', '')
        total_price = request.POST.get('total_price', '')
        guest = request.POST.get('guests', '')

        property = Property.objects.get(id=id)

        Reservation.objects.create(
            property = property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_night,
            total_price=total_price,
            guest=guest,
            created_by = request.user
        )

        return JsonResponse({
            'success': "successfully booked"
        })
    
    except Exception as e:
        print('Error', e)

        return JsonResponse({'sucess': False})


@api_view(['POST'])
def toggle_favorite(request, id):
    try:
        property = Property.objects.get(id=id)
        if request.user in property.favorited.all():
            property.favorited.remove(request.user)
        else:
            property.favorited.add(request.user)
        return JsonResponse({
            'success': 'Property favorited successfully'
        })
    except Property.DoesNotExist:
        return JsonResponse({
            'errors': 'Property not found'
        }, status=404)
    except Exception as e:
        print('Error', e)
        return JsonResponse({
            'errors': 'An error occurred'
        }, status=500)