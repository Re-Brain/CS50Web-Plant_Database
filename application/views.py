from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "application/index.html")

def plantList(request):
    return render(request , "application/plantList.html")

def letterIndexList(request):
    return render(request, "application/letterIndexList.html")

def familyIndexList(request):
    return render(request, "application/familyIndexList.html")