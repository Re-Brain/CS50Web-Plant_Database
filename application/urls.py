from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("plantList", views.plantList, name="plantList"),
    path("familyIndexList", views.familyIndexList, name="familyIndexList"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("plant/<int:id>", views.plantData, name="plant"),
    path("letterIndexList/<str:indexList>", views.letterIndexList, name="letterIndexList"),
    path("familyNameSort/<str:familyName>", views.familyNameSort, name="familyNameSort"),
    path("deletePlant/<int:id>", views.deletePlant , name="deletePlant"),
    path("editPlant/<int:id>", views.editPlant, name="editPlant"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("searchResult", views.searchResult, name='searchResult')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)