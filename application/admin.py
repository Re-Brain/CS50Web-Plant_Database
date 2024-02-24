from django.contrib import admin
from .models import * 

# Register your models here.
class familyNameAdmin(admin.ModelAdmin):
    list_display = ("id", "familyName")

class commonNameAdmin(admin.ModelAdmin):
    list_display = ("id", "commonName")

class plantAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class plantImagesAdmin(admin.ModelAdmin):
    list_display = ("id", "image")

# Register your models here.
admin.site.register(familyName, familyNameAdmin)
admin.site.register(commonName, commonNameAdmin)
admin.site.register(plant, plantAdmin)
admin.site.register(plantImage, plantImagesAdmin)