from django.db import models


class Address(models.Model):
    street = models.CharField(max_length=200)
    street_number = models.CharField(max_length=50, blank=True, null=True)
    city_code = models.CharField(max_length=20, db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    country = models.CharField(max_length=100, default="AT")

    class Meta:
        indexes = [
            models.Index(fields=["city_code", "city"]),
        ]


class AppUser(models.Model):
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Other"))

    first_name = models.CharField(max_length=100, db_index=True)
    last_name = models.CharField(max_length=100, db_index=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, db_index=True)
    customer_id = models.CharField(max_length=50, db_index=True)
    phone_number = models.CharField(max_length=50, db_index=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, related_name="residents"
    )
    birthday = models.DateField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["first_name", "last_name"]),
            models.Index(fields=["customer_id"]),
            models.Index(fields=["created"]),
        ]


class CustomerRelationship(models.Model):
    appuser = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, related_name="relationship"
    )
    points = models.IntegerField(db_index=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["points"]),
            models.Index(fields=["last_activity"]),
        ]
