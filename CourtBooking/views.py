from datetime import datetime

from django.shortcuts import render
from rest_framework.decorators import APIView,api_view
from rest_framework.response import Response
from .serializers import BookingMasterWriteSerializer, CourtMasterSerializer, LocationWithCourtsSerializer , SportMasterSerializer,CourtMasterDetailSerializer,BookingMasterDetailSerializer,BookedSlotViewSerializer,SlotMasterSerializer,BookingMasterSerializer
from .models import CourtMaster,BookingMaster,SlotMaster
from rest_framework import status
from api.utils import get_user_from_token
from .models import SportMaster , UserMaster
from api.serializers import UserSerializer

# Create your views here.


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
        print(sport_name)
        location = request.query_params.get("location",None)
        
        if location is not None and sport_name is not None :
            court = courts.filter(location__city =location , location__sport__name = sport_name)
            print(court)
            serialized_data = CourtMasterDetailSerializer(court , many=True)
            return Response({
            "data":serialized_data.data,
            "status":"Success",
            "statusCode":status.HTTP_200_OK
            })
        
        if sport_name :
            court = courts.filter(location__sport__name = sport_name)
            print(court)
            serialized_data = CourtMasterDetailSerializer(court , many=True)
            return Response({
            "data":serialized_data.data,
            "status":"Success",
            "statusCode":status.HTTP_200_OK
            })
            
        if location :
            court = courts.filter(location__city = location)
            print(court);
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
            courts = courts.filter(location__city__icontains=location_city , user=user_id)

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
                    print(first_courts);
                    
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
        if  court_id is not None:
            booking = BookingMaster.objects.filter(court__court_Id = court_id , book_Date = date)
            serialized_data = BookedSlotViewSerializer(booking , many = True)
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
                
                
    
class CourtBookingSlot(APIView):
    def post(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        slots = request.data.get('slots', [])
        court_id = request.data.get("court_id")
        user_id = request.data.get('user_id')
        date = request.data.get('date')

        if court_id and user_id and date:
            for slot_id in slots:
                slot = SlotMaster.objects.get(slot_Id = slot_id)
                court = CourtMaster.objects.get(court_Id = court_id)
                user = UserMaster.objects.get(reg_id = user_id)
                BookingMaster.objects.create(
                    slot=slot,     # ✅ Use slot_id directly
                    court=court,
                    user=user,
                   book_Date=date
                )

            return Response({
                "status": "success",
                "statusCode": status.HTTP_201_CREATED,
                "data": "Booking confirmed"
            })

        return Response({
            "status": "failed",
            "statusCode": status.HTTP_400_BAD_REQUEST,
            "data": "Parameters required"
        })
               
               
class SeprateUserBookedSlot(APIView):
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response
        
        # Use user from token
        user_id = user.reg_id  
        print(f"Fetching bookings for user_id: {user_id}")

        booked_data = BookingMaster.objects.filter(user=user_id)
        if booked_data.exists():
            serialized_data = BookingMasterDetailSerializer(booked_data, many=True)
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

                
        