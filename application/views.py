from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import plant, familyName
from django.db.models import Q
import string

# from .forms import plantFormTop
# Create your views here.

############### USER ###############
   
############ Listing Pages #############

def index(request):
    return render(request, "application/index.html")

def plantList(request):
    allPlant = plant.objects.all()

    paginator = Paginator(allPlant, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, "application/plantList.html", {"venues" : venues })

def letterIndexList(request, indexList):
    if indexList == "all":
        plants = plant.objects.all()
    else:
        charList = indexList.split('+')
        sortedList = sorted(charList)

        print(sortedList)

        filter_condition = Q()
        for word in sortedList:
            filter_condition |= Q(Q(name__iregex=f'^{word}') | 
                                Q(scientificName__iregex=f'^{word}') | 
                                Q(familyNameList__familyName__iregex=f'^{word}') |
                                Q(commonNameList__commonName__iregex=f'^{word}'))
        
        plants = plant.objects.filter(filter_condition).distinct()

    paginator = Paginator(plants, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, "application/letterIndexList.html", {"venues" : venues , "indexList" : indexList})

    

def familyIndexList(request):
    allFamilyName = familyName.objects.all()
    organized_data = {}

    for uppercase_letter in string.ascii_uppercase:
        organized_data[uppercase_letter] = []

    for name in allFamilyName:
        first_letter = name.familyName[0].upper()
        organized_data[first_letter].append(name)

    for key, value in organized_data.items():
        organized_data[key] = sorted(value, key=lambda x: x.familyName)

    return render(request, "application/familyIndexList.html", {"organized_data" : organized_data})

def familyNameSort(request, familyName):
    allPlant = plant.objects.filter(familyNameList__familyName=familyName)

    paginator = Paginator(allPlant, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, "application/result.html", {"venues" : venues })

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
            # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There was an error login try again"))
            return redirect('login')

    return render(request, "application/login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Successfully logout"))
    return redirect('login')

def dashboard(request):
    if request.user.is_authenticated:
        allPlant = plant.objects.all()

        paginator = Paginator(allPlant, 20)
        page_number = request.GET.get('page')
        venues = paginator.get_page(page_number)

        return render(request, "application/dashboard.html", {"venues" : venues})
    else:
        messages.success(request, ("Please login to use the dashboard"))
        return redirect('login')
    
def plantData(request, id):
    data = plant.objects.get(id=id)
    return render(request, "application/plant.html", {"data" : data })

 