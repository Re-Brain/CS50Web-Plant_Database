from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("plantList", views.plantList, name="plantList"),
    path("letterIndexList", views.letterIndexList, name="letterIndexList"),
    path("familyIndexList", views.familyIndexList, name="familyIndexList"),
]