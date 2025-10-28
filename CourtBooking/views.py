from datetime import datetime, timedelta, timezone

from django.shortcuts import render
from rest_framework.decorators import APIView,api_view
from rest_framework.response import Response

from app_task import release_expired_unpaid_holds
from .serializers import BookingMasterWithAllDataSerializer, BookingMasterWriteSerializer, CourtMasterSerializer, LocationWithCourtsSerializer , SportMasterSerializer,CourtMasterDetailSerializer,BookingMasterDetailSerializer,BookedSlotViewSerializer,SlotMasterSerializer,BookingMasterSerializer , CourtTypeSerializer
from .models import CourtMaster,BookingMaster,SlotMaster, CourtType
from rest_framework import status
from api.utils import get_user_from_token
from .models import SportMaster , UserMaster
from api.serializers import UserSerializer 
from django.db import transaction  
from bookmygame_admin.models import HolidayMaster 



class CourtTypeView(APIView):
    def get(self , request  ):
        user , error_response = get_user_from_token(request)
        if error_response :
            return Response({
                "data":"Token expaired or Not Available",
                "status":"failed",
                "statusCode":status.HTTP_401_UNAUTHORIZED
            })
            
        types = CourtType.objects.all()
        serialized_data = CourtTypeSerializer(types , many = True)
        return Response({
            "data":serialized_data.data,
            "status":"Success",
            "statusCode":status.HTTP_200_OK
            })
        


class CourtView(APIView):
    
    def get(self , request  ):
        user , error_response = get_user_from_token(request)
        if error_response :
            return Response({
                "data":"Token expaired or Not Available",
                "status":"failed",
                "statusCode":status.HTTP_401_UNAUTHORIZED
            })
        courts = CourtMaster.objects.all()   
        sport_name = request.query_params.get('sport',None)
   
        location = request.query_params.get("location",None)
        
        if location is not None and sport_name is not None :
            court = courts.filter(location__city =location , location__sport__name = sport_name)
        
            serialized_data = CourtMasterDetailSerializer(court , many=True)
            return Response({
            "data":serialized_data.data,
            "status":"Success",
            "statusCode":status.HTTP_200_OK
            })
        
        if sport_name :
            court = courts.filter(location__sport__name = sport_name)
       
            serialized_data = CourtMasterDetailSerializer(court , many=True)
            return Response({
            "data":serialized_data.data,
            "status":"Success",
            "statusCode":status.HTTP_200_OK
            })
            
        if location :
            court = courts.filter(location__city = location)
      
            serialized_data = CourtMasterDetailSerializer(court , many=True)
            return Response({
            "data":serialized_data.data,
            "status":"Success",
            "statusCode":status.HTTP_200_OK
            })
              
        # data = CourtMaster.objects.all()
        # courtMaster_serialized = CourtMasterSerializer(data ,many = True)
        return Response({
            "data":"Location not selected",
            "status":"failed",
            "statusCode":status.HTTP_400_BAD_REQUEST
        })
        
        
        
class SportsMasterView(APIView):
   
     def get(self, request ):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response
        
        categories = SportMaster.objects.all()
        serialized_data = SportMasterSerializer(categories, many=True)
        return Response({
            "data": serialized_data.data,
            "status": "success",
            "statusCode": status.HTTP_200_OK
        })
        
        

@api_view(['GET'])
def CourtSeprateView(request, id):
    user, error_response = get_user_from_token(request)
    if error_response:
        return error_response

    court = CourtMaster.objects.filter(court_Id=id)

    if court.exists():
        serialized_data = CourtMasterSerializer(court, many=True)  # or SportMasterSerializer if intended
        return Response({
            "data": serialized_data.data,
            "status": "success",
            "statusCode": status.HTTP_200_OK
        })
    else:
        return Response({
            "data": "No Court Available",
            "status": "failed",
            "statusCode": status.HTTP_404_NOT_FOUND
        })
        

class CourtSelectionView(APIView):
    
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response
        user_id = request.query_params.get('user' , None)
        location_city = request.query_params.get('location',None)

        courts = CourtMaster.objects.filter(flag=True)
        if user_id is not None and location_city is not None:
            courts = courts.filter(location__city__icontains=location_city , user=user_id ,)

            if not courts.exists():
                return Response({
                "status": "failed",
                "statusCode": 404,
                "data": "No Court Available"
            })
          
        # Pick first court per location to represent it
            first_courts = []
            seen_locations = set()
            for court in courts:
                loc_id = court.location.location_Id
                if loc_id not in seen_locations:
                    first_courts.append(court)
                    seen_locations.add(loc_id)
                

                    serializer = LocationWithCourtsSerializer(first_courts, many=True)
                   
                    
                return Response({
                     "status": "success",
                     "statusCode": 200,
                     "data":serializer.data,
                   
                    })


class Slotview(APIView):
    
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response
        
        # user_id = request.query_params.get('user' , None)
        # location_Id = request.query_params.get('location_Id',None)
        court_id = request.query_params.get('court_id', None)
        # date = request.query_params.get('date', None)
        
        
        #unpid  has reverted
        release_expired_unpaid_holds()
        if  court_id is not None:
            slot_view = SlotMaster.objects.filter(court__court_Id = court_id , IsActive = True)
            serialized_data = SlotMasterSerializer(slot_view , many = True)
            
            return Response({
                     "status": "success",
                     "statusCode": status.HTTP_200_OK,
                     "data":serialized_data.data,
                   
                    })
        
        if court_id is None:
                return Response({
                "status": "failed",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "data": "Court No Required"
            })
                
                
                
class BookedSlotCheckView(APIView):
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response
        court_id = request.query_params.get('court_id', None)
        date = request.query_params.get('date', None)
       
        if  court_id is not None and date is not None:
            
            booking = BookingMaster.objects.filter(court__court_Id = court_id , book_Date = date , flag=True)
            serialized_data = BookedSlotViewSerializer(booking , many = True)
            return Response({
                     "status": "success",
                     "statusCode": status.HTTP_200_OK,
                     "data":serialized_data.data,
                   
                    })
        
        if court_id is None and date is None:
                return Response({
                "status": "failed",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "data": "Court No Required"
            })
                
HOLD_DURATION_MINUTES = 10               
    
class CourtBookingSlot(APIView):
    
    @transaction.atomic
    def post(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        slots = request.data.get('slots', [])
        court_id = request.data.get("court_id")
        user_id = request.data.get('user_id')
        date = request.data.get('date')
        amout = request.data.get("amount")
        
        is_booked = BookingMaster.objects.filter(
            court__court_Id=court_id,
            slot_id__in=slots,      # use __in for list of slot IDs
            book_Date=date  ,
         
            flag = True ,
            payment_Id__isnull=False      # assuming your model has a date field
        ).exists()                  # returns True if any matching bookings exist

        if is_booked:
            return Response({"message": "Slot(s) already booked"}, status=400)
        
        expire_at = datetime.now(timezone.utc) + timedelta(minutes=HOLD_DURATION_MINUTES)
        created_ids = []
        if court_id and user_id and date:
            for slot_id in slots:
                slot = SlotMaster.objects.get(slot_Id = slot_id)
                court = CourtMaster.objects.get(court_Id = court_id)
                user = UserMaster.objects.get(reg_id = user_id)
                amount = 0
                if slot.IsPeak :
                    amount = court.peakhours
                    print(amout)
                else :
                    amount = court.nonpeakhours
                    print(amout)
                booking = BookingMaster.objects.create(
                    slot=slot,    
                    court=court,
                    slot_Name = slot.slot_Name,
                    user=user,
                   book_Date=date,
                   flag=True,
                   hold_expires_at = expire_at,
                   final_Amount = float(amount)
                   
                )
                created_ids.append(str(booking.book_Id))

            return Response({
                "status": "success",
                "statusCode": status.HTTP_201_CREATED,
                "data":created_ids
            })

        return Response({
            "status": "failed",
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "data": "Parameters required"
        })
    
    
@api_view(['POST'])
@transaction.atomic
def confirm_booking(request):
    booking_ids = request.data.get('booking_ids', [])
    payment_id = request.data.get('payment_id')

    if not booking_ids or not payment_id:
        return Response({"error":"missing parameters"}, status=status.HTTP_400_BAD_REQUEST)

    bookings = BookingMaster.objects.select_for_update().filter(book_Id__in=booking_ids, )
    if bookings.count() != len(booking_ids):
        return Response({"error":"some bookings not in HOLD state"}, status=status.HTTP_400_BAD_REQUEST)

    for b in bookings:
     
        b.payment_Id = payment_id
        b.hold_expires_at = None
        b.flag = True
        b.save()

    return Response({"status":"confirmed", "booking_ids": booking_ids})


@api_view(['POST'])
@transaction.atomic
def cancel_booking(request):
    booking_ids = request.data.get('booking_ids', [])
    if not booking_ids:
        return Response({"error":"missing booking_ids"}, status=status.HTTP_400_BAD_REQUEST)

    bookings = BookingMaster.objects.select_for_update().filter(book_Id__in=booking_ids)
    for b in bookings:
        b.flag = False
        b.hold_expires_at = None
        b.save()
    return Response({"status":"cancelled", "booking_ids": booking_ids})

               
               
class SeprateUserBookedSlot(APIView):
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response
        
        # Use user from token
        user_id = request.query_params.get("user_id",None)
      
        booked_data = BookingMaster.objects.filter(user__reg_id=user_id)
        print(booked_data)
        if booked_data.exists():
            serialized_data = BookingMasterWithAllDataSerializer(booked_data, many=True)
            return Response({
                "status": "success",
                "statusCode": status.HTTP_200_OK,
                "data": serialized_data.data
            })
        else:
            return Response({
                "status": "success",
                "statusCode": status.HTTP_200_OK,
                "data": []
            })

                
        