from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileForm, PropertyForm, PropertySearchForm
from .models import UserProfile, Property
from .decorators import user_is_landlord

def home(request):
    return render(request, 'home.html')


def property_list(request):
    form = PropertySearchForm()
    properties = Property.objects.all()

    if request.method == 'POST':
        form = PropertySearchForm(request.POST)
        if form.is_valid():
            region = form.cleaned_data['region']
            commune = form.cleaned_data['commune']
            properties = properties.filter(region=region, commune=commune)

    return render(request, 'property_list.html', {'form': form, 'properties': properties})

def property_detail(request, id):
    property = get_object_or_404(Property, id=id)
    return render(request, 'property_detail.html', {'property': property})


@login_required
@user_is_landlord
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        print("Form data received:", request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            return redirect('property_list')
        else:
            print("Form is not valid")
            print("Form errors:", form.errors)
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form': form})

@login_required
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property_list')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'edit_property.html', {'form': form})

@login_required
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        property.delete()
        return redirect('property_list')
    return render(request, 'delete_property.html', {'property': property})  

def search_properties(request):
    form = PropertySearchForm()
    properties = None

    if request.method == 'POST':
        form = PropertySearchForm(request.POST)
        if form.is_valid():
            region = form.cleaned_data['region']
            commune = form.cleaned_data['commune']
            properties = Property.objects.filter(region=region, commune=commune)

    return render(request, 'search_properties.html', {'form': form, 'properties': properties})    

def register(request):
    if request.method == 'POST':
        print('POST data:', request.POST)  
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                print('Authentication failed')
        else:
            print('Form is not valid:', form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})