

from django.urls import path
from . import views

urlpatterns = [
    
  path('court-details/',views.CourtView.as_view(), name="courtview")
    
    
]