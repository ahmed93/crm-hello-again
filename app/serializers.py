from rest_framework import serializers
from .models import Address, AppUser, CustomerRelationship


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class AppUserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = AppUser
        fields = "__all__"


class CustomerRelationshipSerializer(serializers.ModelSerializer):
    appuser = AppUserSerializer(read_only=True)

    class Meta:
        model = CustomerRelationship
        fields = "__all__"
