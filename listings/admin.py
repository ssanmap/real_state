from django.contrib import admin
from .models import Region, Commune, PropertyType, Property, UserType, UserProfile

admin.site.register(Region)
admin.site.register(Commune)
admin.site.register(PropertyType)
admin.site.register(Property)
admin.site.register(UserType)
admin.site.register(UserProfile)