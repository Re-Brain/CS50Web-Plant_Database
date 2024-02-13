from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from .models import plant, familyName, plantImage, qrImage, commonName
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
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

    return render(request, "application/plantList.html", {"venues" : venues})

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

    title = "Familyname: " + familyName

    paginator = Paginator(allPlant, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, "application/result.html", {"venues" : venues , "title" : title})

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
        admin = True
        title = "Dashboard"

        paginator = Paginator(allPlant, 20)
        page_number = request.GET.get('page')
        venues = paginator.get_page(page_number)

        return render(request, "application/dashboard.html", {"venues" : venues , "admin" : admin , "title" : title })
    else:
        messages.success(request, ("Please login to use the dashboard"))
        return redirect('login')
    
def plantData(request, id):
    data = plant.objects.get(id=id)
    return render(request, "application/plant.html", {"data" : data })

def deletePlant(request, id):
    deletePlant = plant.objects.get(id=id)

    if request.method == 'DELETE':
        deletePlant.delete()
        return HttpResponseRedirect(reverse("dashboard"))
    
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def editPlant(request, id):
    editPlant = plant.objects.get(id=id)
    edit = True
    title = "Edit:"

    return render(request, "application/edit.html", {"plant" : editPlant, "edit" : edit, "title" : title})

def deleteImage(request, id):
    deleteImage = plantImage.objects.get(id=id)

    if request.method == 'DELETE':
        deleteImage.delete()
        return JsonResponse({'message': 'Image deleted successfully.'})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def deleteQR(request, id):
    deleteQR = qrImage.objects.get(id=id)

    if request.method == 'DELETE':
        deleteQR.delete()
        return JsonResponse({'message': 'Image deleted successfully.'})

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def create(request):
    title = "Create"
    if request.method == "POST":
        name = request.POST.get('name')
        scientificName = request.POST.get('scientific-name')
        familyNames = request.POST.getlist('family-name')
        commonNames = request.POST.getlist('common-name')
        use = request.POST.get('use')
        characteristic = request.POST.get('characteristic')
        distribution = request.POST.get('distribution')
        habitat = request.POST.get('habitat')
        care = request.POST.get('care')
        location = request.POST.get('location')
        reference = request.POST.get('reference')
        qrImages = request.FILES.getlist('qr-input')
        plantImages = request.FILES.getlist('image-input')

        print(name, scientificName, familyNames, commonNames, use
              , characteristic , distribution, habitat, care, location, reference, qrImages, plantImages)

        newPlant = plant.objects.create(name=name, scientificName=scientificName
                        , uses=use, characteristic=characteristic, 
                        distribution=distribution, habitat=habitat,
                        care=care, location=location, references=reference)
         
        for name in familyNames:
            if name != '':
                nameInstance, create = familyName.objects.get_or_create(familyName=name)
                newPlant.familyNameList.add(nameInstance)

        for name in commonNames:
            if name != '':
                nameInstance, create = commonName.objects.get_or_create(commonName=name)
                newPlant.commonNameList.add(nameInstance)
        
        for image in qrImages:
            imageInstance = qrImage.objects.create(image=image)
            newPlant.qrImageList.add(imageInstance)

        for image in plantImages:
            imageInstance = plantImage.objects.create(image=image)
            newPlant.plantImageList.add(imageInstance)

        return render(request, "application/create.html", { "title" : title})
   
    return render(request, "application/create.html", { "title" : title})




 