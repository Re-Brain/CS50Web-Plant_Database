from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Main page
    path("", views.index, name="index"),
    path("plantList", views.plantList, name="plantList"),
    
    path("letterIndexList/<str:indexList>", views.letterIndexList, name="letterIndexList"),

    path("familyIndexList", views.familyIndexList, name="familyIndexList"),
    path("familyNameSort/<str:familyName>", views.familyNameSort, name="familyNameSort"),

    # Plant data page
    path("plant/<int:id>", views.plantData, name="plant"),

    # Search option system
    path("search", views.search, name="search"),
    path("searchResult", views.searchResult, name='searchResult'),
    path("searchResult/<str:input>", views.searchResult, name="searchResult"),

    path("advanceSearch", views.advanceSearch, name="advanceSearch"),
    path("advanceSearchResult/<str:name>/<str:scientificName>/<str:familyName>/<str:commonName>"
         , views.advanceSearchResult, name="advanceSearchResult"),

    # Login page and logout system
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),

    # Admin system
    path("dashboard", views.dashboard, name="dashboard"),
    path("deletePlant/<int:id>", views.deletePlant , name="deletePlant"),
    path("editPlant/<int:id>", views.editPlant, name="editPlant"),
    
    # Admin search system
    path("adminSearch", views.adminSearch, name="adminSearch"),
    path("adminSearchResult/<str:input>", views.adminSearchResult, name="adminSearchResult"),
    
    path("create", views.create, name="create")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)