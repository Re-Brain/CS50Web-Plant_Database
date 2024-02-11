from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("plantList", views.plantList, name="plantList"),
    path("letterIndexList", views.letterIndexList, name="letterIndexList"),
    path("familyIndexList", views.familyIndexList, name="familyIndexList"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("plant/<int:id>", views.plantData, name="plant"),
    path("list/<str:familyName>", views.list, name="list")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)