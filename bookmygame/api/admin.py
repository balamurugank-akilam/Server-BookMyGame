from django.contrib import admin
from .models import SportCategory,UserMaster , UserTypeMaster
# Register your models here.

admin.site.register(SportCategory)
admin.site.register(UserTypeMaster)
admin.site.register(UserMaster)