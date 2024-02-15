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
from django.db.models.signals import post_delete
from django.dispatch import receiver
import json
import os
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
        familyNameCommonNameChecker()

        for image in deletePlant.qrImageList.all():
            os.remove(image.image.path)

        for image in deletePlant.plantImageList.all():
            os.remove(image.image.path)

        deletePlant.delete()

        return HttpResponseRedirect(reverse("dashboard"))
    
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def familyNameCommonNameChecker():
    allFamilyName = familyName.objects.all()
    allCommonName = commonName.objects.all()
    
    orphansFamily = allFamilyName.filter(famName__isnull=True)
    orphansCommon = allCommonName.filter(comName__isnull=True)

    orphansFamily.delete()
    orphansCommon.delete()

@csrf_exempt
def search(request):

    if 'search' in request.POST:
        print("normal")
        request.session['input'] = request.POST.get('search')
    
    elif 'adminSearch' in request.POST:
        print("admin")
        request.session['input'] = request.POST.get('adminSearch')
        request.session['admin'] = request.POST.get('admin')
    else:
        request.session['advanceSearch-name'] = request.POST.get('advanceSearch-name')
        request.session['advanceSearch-scientific-name'] = request.POST.get('aadvanceSearch-scientific-name')
        request.session['advanceSearch-family-name'] = request.POST.get('advanceSearch-family-name')
        request.session['advanceSearch-common-name'] = request.POST.get('advanceSearch-common-name')

    return HttpResponseRedirect(reverse('searchResult'))

def searchResult(request):
       
    if request.session.get('input'):
        input = request.session.get('input')
        print("inputResult")

        filteredPlant = plant.objects.filter(
        Q(name__icontains=input) | Q(scientificName__icontains=input)
        | Q(familyNameList__familyName__icontains=input) | Q(commonNameList__commonName__icontains=input)
        ).distinct()

    elif (request.session.get('advanceSearch-name') and request.session.get['advanceSearch-scientific-name'] and 
        request.session.get['advanceSearch-family-name'] and request.session.get['advanceSearch-common-name']):

        print("inputAdvance")

        name = request.seesion.get('advanceSearch-name')
        scientificName = request.session.get['advanceSearch-scientific-name']
        familyName = request.session.get['advanceSearch-family-name']
        commonName = request.session.get['advanceSearch-common-name']

        filteredPlant = plant.objects.filter(
        Q(name__icontains=name) | Q(scientificName__icontains=scientificName)
        | Q(familyNameList__familyName__icontains=familyName) | Q(commonNameList__commonName__icontains=commonName)
        ).distinct()
    
    paginator = Paginator(filteredPlant, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    if request.session.get('admin') == 'admin':
        admin = True
        return render(request, "application/adminResult.html", {"venues" : venues, "admin" : admin})
    
    print("normalResult")
    return render(request, "application/result.html", {"venues" : venues})

@csrf_exempt
def editPlant(request, id):
    editPlant = plant.objects.get(id=id)
    edit = True
    title = "Edit:"

    if request.method == "POST":
        plantID = request.POST.get('id')
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
        existQRImages = request.POST.getlist('qr-image-info')
        existPlantImages = request.POST.getlist('plant-image-info')

        existPlant = plant.objects.get(id=plantID)
        existPlant.name = name
        existPlant.scientificName = scientificName
        existPlant.uses = use
        existPlant.characteristic = characteristic
        existPlant.distribution = distribution
        existPlant.habitat = habitat
        existPlant.care = care
        existPlant.location = location
        existPlant.references = reference

        # Clear the existed item in familyNames before adding new values
        for name in existPlant.familyNameList.all():
            if name.familyName not in familyNames:
                name_to_remove = familyName.objects.get(familyName=name.familyName)
                existPlant.familyNameList.remove(name_to_remove)
                relate_instance_count = plant.objects.filter(familyNameList__familyName=name.familyName).count()
                if relate_instance_count == 0:
                    name_to_remove.delete()


        for name in familyNames:
            if name != '':
                nameInstance, create = familyName.objects.get_or_create(familyName=name)
                existPlant.familyNameList.add(nameInstance)

        
        
        # Clear the existed item in commonNames before adding new values
        for name in existPlant.commonNameList.all():
            if name.commonName not in commonNames:
                name_to_remove = commonName.objects.get(commonName=name.commonName)
                existPlant.commonNameList.remove(name_to_remove)
                relate_instance_count = plant.objects.filter(commonNameList__commonName=name.commonName).count()
                if relate_instance_count == 0:
                    name_to_remove.delete()

        for name in commonNames:
            if name != '':
                nameInstance, create = commonName.objects.get_or_create(commonName=name)
                existPlant.commonNameList.add(nameInstance)


        # Clear the existed item in qrImageList that delete by user before adding new values
        for image in existPlant.qrImageList.all():
            if str(image.id) not in existQRImages:
                image_to_remove = qrImage.objects.get(id=image.id)
                existPlant.qrImageList.remove(image_to_remove)
                os.remove(image_to_remove.image.path)
                image_to_remove.delete()
                existPlant.save()

        for image in qrImages:
            imageInstance = qrImage.objects.create(image=image)
            existPlant.qrImageList.add(imageInstance)

        # Clear the existed item in plantImageList that delete by user before adding new values
        for image in existPlant.plantImageList.all():
            if str(image.id) not in existPlantImages:
                image_to_remove = plantImage.objects.get(id=image.id)
                existPlant.plantImageList.remove(image_to_remove)
                os.remove(image_to_remove.image.path)
                image_to_remove.delete()
                existPlant.save()

        for image in plantImages:
            imageInstance = plantImage.objects.create(image=image)
            existPlant.plantImageList.add(imageInstance)

        messages.success(request, ("The information about the plant has been edited"))

        return render(request, "application/edit.html", {"plant" : existPlant, "edit" : edit, "title" : title})

    return render(request, "application/edit.html", {"plant" : editPlant, "edit" : edit, "title" : title})

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

        messages.success(request, ("A new plant has been added to the database"))

        return render(request, "application/create.html", { "title" : title})
   
    return render(request, "application/create.html", { "title" : title})




 