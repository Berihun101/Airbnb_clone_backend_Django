from .models  import User

from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from .serializers import UserDetailSerializer
from property.serializers import ReservationsListSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])

def landlord_detail(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def reservation_list(request):
    reservations = request.user.reservations.all()
    serialiazer = ReservationsListSerializer(reservations, many=True)

    return JsonResponse(serialiazer.data, safe=False)


