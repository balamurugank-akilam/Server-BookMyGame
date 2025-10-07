from django.contrib import admin
from .models import UserMaster , UserTypeMaster
# Register your models here.


admin.site.register(UserTypeMaster)
admin.site.register(UserMaster)