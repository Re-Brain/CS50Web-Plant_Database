from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

############### USER ###############
   
############ Listing Pages #############

def index(request):
    return render(request, "application/index.html")

def plantList(request):
    return render(request , "application/plantList.html")

def letterIndexList(request):
    return render(request, "application/letterIndexList.html")

def familyIndexList(request):
    return render(request, "application/familyIndexList.html")

def register(request):
    return render(request, 'application/register.html')