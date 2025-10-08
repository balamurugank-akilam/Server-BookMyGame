

from django.urls import path
from . import views

urlpatterns = [
    
  path('court-details/',views.CourtView.as_view(), name="courtview"),
  path('sports',views.SportsMasterView.as_view(),name="sportsMasterView"),
  path('seperate-court/<int:id>/', views.CourtSeprateView, name='court-seperate'),
  path('court-selection/',views.CourtSelectionView.as_view(),name='court_selection'),
  
    
]