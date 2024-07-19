from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile, UserType
from django_select2.forms import Select2Widget
from .models import Property , Region, Commune

class CustomUserCreationForm(UserCreationForm):
    rut = forms.CharField(max_length=9)
    address = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=50)
    user_type = forms.ModelChoiceField(queryset=UserType.objects.all())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'rut', 'address', 'phone', 'user_type')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                rut=self.cleaned_data['rut'],
                address=self.cleaned_data['address'],
                phone=self.cleaned_data['phone'],
                user_type=self.cleaned_data['user_type'],
            )
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'address', 'phone', 'user_type')

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'name', 'description', 'constructed_area', 'land_area', 'num_parking_spaces', 
            'num_bedrooms', 'num_bathrooms', 'address', 'monthly_price', 'commune', 
            'region', 'property_type', 'rented'
        ]

class PropertySearchForm(forms.Form):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    commune = forms.ModelChoiceField(
        queryset=Commune.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def search(self):
        properties = Property.objects.all()
        if self.is_valid():
            if self.cleaned_data['region']:
                properties = properties.filter(region=self.cleaned_data['region'])
            if self.cleaned_data['commune']:
                properties = properties.filter(commune=self.cleaned_data['commune'])
        return properties