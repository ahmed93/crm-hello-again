from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Address, AppUser, CustomerRelationship
from .serializers import (
    AddressSerializer,
    AppUserSerializer,
    CustomerRelationshipSerializer,
)


@method_decorator(cache_page(60), name="list")
class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all().order_by("id")
    serializer_class = AddressSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["street", "city", "city_code"]
    ordering_fields = ["city", "id"]


@method_decorator(cache_page(60), name="list")
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


@method_decorator(cache_page(60), name="list")
class CustomerRelationshipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        CustomerRelationship.objects.select_related("appuser").all().order_by("id")
    )
    serializer_class = CustomerRelationshipSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["points", "last_activity"]


@method_decorator(cache_page(60), name="list")
class AppUserJoinedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        AppUser.objects.select_related("address")
        .prefetch_related(
            Prefetch("relationship", queryset=CustomerRelationship.objects.all())
        )
        .all()
        .order_by("id")
    )

    serializer_class = AppUserSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = {
        "first_name": ["exact", "icontains"],
        "last_name": ["exact", "icontains"],
        "gender": ["exact"],
        "customer_id": ["exact"],
        "created": ["gte", "lte"],
    }

    search_fields = [
        "first_name",
        "last_name",
        "phone_number",
        "customer_id",
        "address__city",
    ]

    ordering_fields = [
        "first_name",
        "last_name",
        "created",
        "gender",
        "relationship__points",
    ]
