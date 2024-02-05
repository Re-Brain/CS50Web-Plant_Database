from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .forms import plantFormTop
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
        return render(request, "application/dashboard.html")
    else:
        messages.success(request, ("Please login to use the dashboard"))
        return redirect('login')

# def create(request):
#     form = plantFormTop
#     return render(request, 'application/create.html', {'form' : form})