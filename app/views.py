from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Address, AppUser, CustomerRelationship
from .serializers import (
    AddressSerializer,
    AppUserSerializer,
    CustomerRelationshipSerializer,
)

class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all().order_by("id")
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["street", "city", "city_code"]
    ordering_fields = ["city", "id"]


class AppUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AppUser.objects.select_related("address").all().order_by("id")
    serializer_class = AppUserSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["first_name", "last_name", "gender", "customer_id"]
    search_fields = ["first_name", "last_name", "phone_number"]
    ordering_fields = ["first_name", "last_name", "created"]


class CustomerRelationshipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        CustomerRelationship.objects.select_related("appuser").all().order_by("id")
    )
    serializer_class = CustomerRelationshipSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["points", "last_activity"]
