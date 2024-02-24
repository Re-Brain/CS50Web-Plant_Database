from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from .models import plant, familyName, plantImage, commonName
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
import string

# Create your views here.

# home page
def index(request):
    return render(request, "application/index.html")

# all plant list page
def plantList(request):
    allPlant = plant.objects.all() # List all the plant in the database
 
    # Create pagination data 
    paginator = Paginator(allPlant, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, "application/plantList.html", {"venues" : venues}) 

# letter index list page
def letterIndexList(request, indexList):
    if indexList == "all": # Initial page when no button apply
        plants = plant.objects.all() 
    else: # When some button was clicked
        charList = indexList.split('+')
        sortedList = sorted(charList)

        filter_condition = Q()
        for word in sortedList:
            filter_condition |= Q(Q(name__iregex=f'^{word}') | 
                                Q(scientificName__iregex=f'^{word}') | 
                                Q(familyNameList__familyName__iregex=f'^{word}') |
                                Q(commonNameList__commonName__iregex=f'^{word}'))
        
        plants = plant.objects.filter(filter_condition).distinct() # Data filterd based on the button

    # Create pagination data 
    paginator = Paginator(plants, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, "application/letterIndexList.html", {"venues" : venues , "indexList" : indexList})

# family index list page
def familyIndexList(request):
    allFamilyName = familyName.objects.all()
    organized_data = {} # Organize data by using alphabet

    for uppercase_letter in string.ascii_uppercase: # Assign each key value (A-Z)
        organized_data[uppercase_letter] = []

    for name in allFamilyName: # Assign each value in familyName based on the first alphabet to put in each key value
        first_letter = name.familyName[0].upper()
        organized_data[first_letter].append(name)

    for key, value in organized_data.items(): # Sorted each array
        organized_data[key] = sorted(value, key=lambda x: x.familyName)

    return render(request, "application/familyIndexList.html", {"organized_data" : organized_data})

# List result contains all plant with same familyName
def familyNameSort(request, familyName):
    # Plants with same family name
    allPlant = plant.objects.filter(familyNameList__familyName=familyName)

    title = "Familyname: " + familyName

     # Create pagination data 
    paginator = Paginator(allPlant, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, "application/result.html", {"venues" : venues , "title" : title})

# the login page
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if not username or not password: # if the username or password is not filled
            messages.error(request, "กรุณากรอกทั้งชื่อและรหัสผ่าน")
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)

        if user is not None: # if the user was not in the system
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, ("ชื่อหรือรหัสผ่านมีข้อผิดพลาด"))
            return redirect('login')

    return render(request, "application/login.html", {})

# the logout system
def logout_user(request):
    logout(request)
    messages.success(request, ("Successfully logout"))
    return redirect('login')

# admin dashboard page
def dashboard(request):
    if request.user.is_authenticated: # if user login to the system
        allPlant = plant.objects.all()
        admin = True
        title = "ฐานข้อมูลพรรณไม้"

        paginator = Paginator(allPlant, 20)
        page_number = request.GET.get('page')
        venues = paginator.get_page(page_number)

        return render(request, "application/dashboard.html", {"venues" : venues , "admin" : admin , "title" : title })
    else:
        messages.success(request, ("Please login to use the dashboard"))
        return redirect('login')

# Plant data page
def plantData(request, id):
    data = plant.objects.get(id=id)
    return render(request, "application/plant.html", {"data" : data })

# delte plant system
def deletePlant(request, id):
    deletePlant = plant.objects.get(id=id)

    if request.method == 'DELETE':
        familyNameCommonNameChecker()

        for image in deletePlant.plantImageList.all():
            os.remove(image.image.path)

        deletePlant.delete()

        return HttpResponseRedirect(reverse("dashboard"))
    
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

# delete commonName and familyName that isn't use
def familyNameCommonNameChecker():
    allFamilyName = familyName.objects.all()
    allCommonName = commonName.objects.all()
    
    orphansFamily = allFamilyName.filter(famName__isnull=True)
    orphansCommon = allCommonName.filter(comName__isnull=True)

    orphansFamily.delete()
    orphansCommon.delete()

# normal Search engine page
@csrf_exempt
def search(request):
    input = request.POST.get('input')

    if not input:
        input = None
    
    return redirect('searchResult', input=input)
 
# normal search engine system
def searchResult(request, input):
    
    filteredPlant = plant.objects.filter(
        Q(name__icontains=input) | Q(scientificName__icontains=input)
        | Q(familyNameList__familyName__icontains=input) | Q(commonNameList__commonName__icontains=input)
        ).distinct()
    
    paginator = Paginator(filteredPlant, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, "application/result.html", {"venues" : venues})

# advance search engine page
@csrf_exempt
def advanceSearch(request):
    name = request.POST.get('name')
    scientificName = request.POST.get('scientific-name')
    familyName = request.POST.get('family-name')
    commonName = request.POST.get('common-name')

    if not name:
        name = None

    if not scientificName:
        scientificName = None

    if not familyName:
        familyName = None
    
    if not commonName:
        commonName = None

    return redirect('advanceSearchResult', name=name, scientificName=scientificName,
                    familyName=familyName, commonName=commonName)

# advance search engine system
def advanceSearchResult(request, name, scientificName, familyName, commonName):
    filteredPlant = plant.objects.filter(
        Q(name__icontains=name) | Q(scientificName__icontains=scientificName)
        | Q(familyNameList__familyName__icontains=familyName) | Q(commonNameList__commonName__icontains=commonName)
        ).distinct()
    
    paginator = Paginator(filteredPlant, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, "application/result.html", {"venues" : venues})

# admin search engine page
@csrf_exempt
def adminSearch(request):
    if request.user.is_authenticated:
        input = request.POST.get('input')

        if not input:
            input = None
            
        return redirect('adminSearchResult', input=input)
    else:
        messages.success(request, ("Please login to use the dashboard"))
        return redirect('login')

# admin search engine system
def adminSearchResult(request, input):
    filteredPlant = plant.objects.filter(
        Q(name__icontains=input) | Q(scientificName__icontains=input)
        | Q(familyNameList__familyName__icontains=input) | Q(commonNameList__commonName__icontains=input)
        ).distinct()
    
    paginator = Paginator(filteredPlant, 20)
    page_number = request.GET.get('page')
    venues = paginator.get_page(page_number)

    return render(request, "application/adminResult.html", {"venues" : venues, "admin" : True})

# edit plant page and system
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

        messages.success(request, ("ข้อมูลพืชได้รับการแก้ไข"))

        return render(request, "application/edit.html", {"plant" : existPlant, "edit" : edit, "title" : title})

    return render(request, "application/edit.html", {"plant" : editPlant, "edit" : edit, "title" : title})

# edit plant page and system
@csrf_exempt
def create(request):
    title = "เพิ่มข้อมูล"
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
        plantImages = request.FILES.getlist('image-input')

        print(name, scientificName, familyNames, commonNames, use
              , characteristic , distribution, habitat, care, location, reference, plantImages)

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

        for image in plantImages:
            imageInstance = plantImage.objects.create(image=image)
            newPlant.plantImageList.add(imageInstance)

        messages.success(request, ("ข้อมูลพืชตัวใหม่ได้ถูกเพิ่มเข้าไปในฐานข้อมูล"))

        return render(request, "application/create.html", { "title" : title})
   
    return render(request, "application/create.html", { "title" : title})




 