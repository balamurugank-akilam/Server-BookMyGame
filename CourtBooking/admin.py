from django.contrib import admin
from .models import CourtMaster , LocationMaster , SlotMaster , BookingMaster
# Register your models here.

admin.site.register(CourtMaster)
admin.site.register(LocationMaster)
admin.site.register(SlotMaster)
admin.site.register(BookingMaster)
