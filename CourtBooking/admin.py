from django.contrib import admin
from .models import CourtMaster , LocationMaster , SlotMaster , BookingMaster , SportMaster,SportCategory,CourtType,SessionMaster
# Register your models here.
admin.site.register(SportMaster)
admin.site.register(SportCategory)
admin.site.register(CourtMaster)
admin.site.register(LocationMaster)
admin.site.register(SlotMaster)
admin.site.register(BookingMaster)
admin.site.register(CourtType)
admin.site.register(SessionMaster)
   