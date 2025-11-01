

from django.urls import path
from . import views

urlpatterns = [
    
  path('court-details/',views.CourtView.as_view(), name="courtview"),
  path('sports',views.SportsMasterView.as_view(),name="sportsMasterView"),
  path('seperate-court/<int:id>/', views.CourtSeprateView, name='court-seperate'),
  path("court-Type", views.CourtTypeView.as_view() , name = 'Court-type'),
  path('court-selection/',views.CourtSelectionView.as_view(),name='court_selection'),
  path('slot-view/',views.Slotview.as_view() , name='slot-view'), # get slots
  path('booked-slot/',views.BookedSlotCheckView.as_view() , name='booked-slot'),
  path('slot-booking/',views.CourtBookingSlot.as_view(),name='slot-booking'),
  path('user-bookedslotView/',views.SeprateUserBookedSlot.as_view(), name='user-bookedSlotView'),
  path('confirm-booking',views.confirm_booking , name='confirm-booking'),
  path('cancel-booking/',views.cancel_booking , name='cancel-booking'),
  path("slot-holiday-check/",views.SlotHolidayCheck , name="slot-holiday-check"),

  
    
]