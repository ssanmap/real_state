from django.db import models
from django.contrib.auth.models import User


class UserType(models.Model):
    name = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.id} {self.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    rut = models.CharField(max_length=9, primary_key=True)
    address = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=50, null=False, blank=False)
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.rut}"

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Commune(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PropertyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Property(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    constructed_area = models.FloatField(null=False)
    land_area = models.FloatField(null=False)
    num_parking_spaces = models.IntegerField(default=0)
    num_bedrooms = models.IntegerField(default=0)
    num_bathrooms = models.IntegerField(default=0)
    address = models.CharField(max_length=50, null=False, blank=False)
    monthly_price = models.FloatField(null=False)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, null=False)
    rented = models.BooleanField(default=False)

    def __str__(self):
        return self.name

