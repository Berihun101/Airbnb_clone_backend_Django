from django.urls import path

from . import api


urlpatterns = [
    path('', api.properties_list, name='api_properties_list'),
    path('create/', api.create_property, name='api_create_property'),
    path('<uuid:id>/', api.property_detail, name='api_property_detail'),
    path('<uuid:id>/book/', api.book_property, name='api_book_property'),
    path('<uuid:id>/reservations/', api.property_reservation, name='api_property_reservation'),
    path('<uuid:id>/toggle_favorite/', api.toggle_favorite, name='api_toggle_favorite'),
]