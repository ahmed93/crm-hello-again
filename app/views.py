from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
import django_filters

from .models import Address, AppUser, CustomerRelationship
from .serializers import (
    AddressSerializer,
    AppUserSerializer,
    CustomerRelationshipSerializer,
)


class AppUserFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name="address__city", lookup_expr="icontains")
    city_code = django_filters.CharFilter(field_name="address__city_code", lookup_expr="exact")

    class Meta:
        model = AppUser
        fields = {
            "first_name": ["exact", "icontains"],
            "last_name": ["exact", "icontains"],
            "gender": ["exact"],
            "customer_id": ["exact"],
            "created": ["gte", "lte"],
            "phone_number": ["exact", "icontains"],
            "birthday": ["exact", "gte", "lte"],
            "last_updated": ["gte", "lte"],

            # Address fields
            "address__city": ["exact", "icontains"],
            "address__city_code": ["exact"],
            "address__street": ["exact", "icontains"],
            "address__street_number": ["exact"],
            "address__country": ["exact"],

            # Relationship fields
            "relationship__points": ["gte", "lte", "exact"],
            "relationship__created": ["gte", "lte"],
            "relationship__last_activity": ["gte", "lte"],
        }


@method_decorator(cache_page(60), name="list")
class AddressViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Address.objects.all().order_by("id")
    serializer_class = AddressSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "street": ["exact", "icontains"],
        "city": ["exact", "icontains"],
        "city_code": ["exact"],
        "country": ["exact"],
    }
    search_fields = ["street", "city", "city_code"]
    ordering_fields = ["city", "id"]


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
        .distinct()
    )

    serializer_class = AppUserSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = AppUserFilter

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
        "customer_id",
        "phone_number",
        "birthday",
        "last_updated",
        "address__city",
        "address__city_code",
        "address__street",
        "address__country",
        "relationship__points",
        "relationship__created",
        "relationship__last_activity",
    ]
