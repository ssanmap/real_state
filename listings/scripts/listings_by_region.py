import os
import sys
import django
sys.path.append('/Users/ssanmartinp/Documents/cPYTHON/m7/h2/real_state')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_state.settings')
django.setup()

from listings.models import Property, Region

with open('properties_by_region.txt', 'w') as file:
    regions = Region.objects.all()
    for region in regions:
        properties = Property.objects.filter(commune__region=region)
        file.write(f"Region: {region.name}\n")
        for property in properties:
            file.write(f"\tName: {property.name}, Description: {property.description}\n")
