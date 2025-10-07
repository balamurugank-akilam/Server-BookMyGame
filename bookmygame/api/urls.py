

from django.urls import path
from . import views

urlpatterns = [
    
    path("sports/",views.SportsCategoryView.as_view(), name="SportsCategory"),
    path("login/",views.UserLogin.as_view(),name="UserLogin")
    
    
]