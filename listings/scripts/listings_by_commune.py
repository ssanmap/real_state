import os
import sys
import django
sys.path.append('/Users/ssanmartinp/Documents/cPYTHON/m7/h2/real_state')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_state.settings')
django.setup()

from listings.models import Property, Commune

with open('properties_by_commune.txt', 'w') as file:
    communes = Commune.objects.all()
    for commune in communes:
        properties = Property.objects.filter(commune=commune)
        file.write(f"Commune: {commune.name}\n")
        for property in properties:
            file.write(f"\tName: {property.name}, Description: {property.description}\n")
