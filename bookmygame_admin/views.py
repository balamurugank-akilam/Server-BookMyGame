from django.shortcuts import render
from api.utils import get_user_from_token
from rest_framework.decorators import APIView
from rest_framework.response import Response
from api.models import UserMaster , UserTypeMaster 
from CourtBooking.models import CourtMaster,SlotMaster,BookingMaster
from CourtBooking.models import LocationMaster
from CourtBooking.serializers import LocationMasterDetailSerializer , CourtMasterDetailSerializer , SlotMasterSerializer , BookingMasterDetailSerializer , BookingMasterWithAllDataSerializer
from rest_framework import status
from django.apps import apps
from app_task import CreateTimeslots
from .models import HolidayMaster
from .serializers import HolidayMasterSerializer

# Create your views here.

class AdminLogin(APIView):
    def post(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response
        
        email = request.data.get("email" , None)
        password = request.data.get("password" , None)
        
        # role = UserTypeMaster.objects.get(id = 2)
        user = UserMaster.objects.filter(email=email, password=password, user_type__id=2).first()

        if not user:  # True if no user with type=2 and matching credentials
            return Response({
        "data": "User not valid or not admin",
        "status": "failed",
        "statusCode": status.HTTP_401_UNAUTHORIZED
    })
        else:
            return Response({
        "data": "Login successfully",
        "status": "success",
        "statusCode": status.HTTP_200_OK
    })



class AdminLocationView(APIView):
    
    def post(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response
        
        is_user_admin = UserMaster.objects.filter(reg_id = user.reg_id , user_type__id=2) 

        if not is_user_admin:  # True if no user with type=2 and matching credentials
            return Response({
        "data": "User not valid or not admin",
        "status": "failed",
        "statusCode": status.HTTP_401_UNAUTHORIZED
    })
        serialzer_data = LocationMasterDetailSerializer(data = request.data)
        if serialzer_data.is_valid():
            data = serialzer_data.save()
            
            return Response({
        "data": serialzer_data.data,
        "status": "success",
        "statusCode": status.HTTP_200_OK
    })
            
        else:
            return Response({
        "data": "form not valid",
        "status": "failed",
        "statusCode": status.HTTP_401_UNAUTHORIZED
    })
            
    def get(self , request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response
        
        is_user_admin = UserMaster.objects.filter(reg_id = user.reg_id , user_type__id=2) 

        if not is_user_admin:  # True if no user with type=2 and matching credentials
            return Response({
        "data": "User not valid or not admin",
        "status": "failed",
        "statusCode": status.HTTP_401_UNAUTHORIZED
    })
        
        try:
           model = apps.get_model("CourtBooking", "LocationMaster")  
        except LookupError:
            return Response({
                "data": f"Model '{LocationMaster}' not found",
                "status": "failed",
                "statusCode": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        exclude_fields = ['flag', 'reg_Id', 'location_Id']
        fields = []

        for field in LocationMaster._meta.get_fields():
            # Skip auto-created reverse relationships (many-to-one) and one-to-many fields
            if field.many_to_one and field.auto_created:
                continue
            if field.one_to_many:
                continue

            # Skip fields listed in exclude_fields
            if field.name in exclude_fields:
                continue

            # Add the field name to the list
            fields.append(field.name)

        print(fields)

        location_data = LocationMaster.objects.filter(reg_Id = user.reg_id)
        serialized = LocationMasterDetailSerializer(location_data , many =True)


       
        return Response({
        
            "fields": fields,
            "data":serialized.data,
            "status": "success",
            "statusCode": status.HTTP_200_OK
        })
        
    
    def put(self , request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        is_user_admin = UserMaster.objects.filter(reg_id=user.reg_id, user_type__id=2).exists()
        if not is_user_admin:
            return Response({
                "data": "User not valid or not admin",
                "status": "failed",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            }) 
            
        location_id = request.data.get("location_Id")
        if not location_id :
            return Response({
                'status':"failed",
                "statusCode":status.HTTP_400_BAD_REQUEST,
                "data":"location id required"
            })
            
        location = LocationMaster.objects.get(location_Id = location_id)
        serialized_data = LocationMasterDetailSerializer(location , data= request.data , partial = True)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({
                "data":"data updated",
                "status":"success",
                "statusCode":status.HTTP_202_ACCEPTED
            })
            
        else :
            return Response({
                "data" : "Invalid data",
                "status":"failed",
                "statusCode":status.HTTP_400_BAD_REQUEST
            })
        

    def delete(self , request):
        
        location_id = request.data.get("location_id")
        
        if location_id is not None :
            location = LocationMaster.objects.filter(location_Id = location_id)
            location.delete()
            return Response({
            "data":"Location Deleted ",
            "status": "success",
            "statusCode": status.HTTP_200_OK
        })
            
        return Response({
                "data": f"parameters Required",
                "status": "failed",
                "statusCode": status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)
        
        
        
        
class AdminCourtView(APIView):
    def post(self, request, *args, **kwargs):
       
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        is_user_admin = UserMaster.objects.filter(reg_id=user.reg_id, user_type__id=2).exists()
        if not is_user_admin:
            return Response({
                "data": "User not valid or not admin",
                "status": "failed",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            })

      
        court_serializer = CourtMasterDetailSerializer(data=request.data)

       
        if court_serializer.is_valid():
           
            validated_court = court_serializer.validated_data
            start_time = validated_court.get("starttime")
            end_time = validated_court.get("endtime")
            slot_time = validated_court.get("duration")
      
          
            court_instance = court_serializer.save()
            time_slot_creator = CreateTimeslots()
            time_slot_creator.basicTimeslot(
                startTime=start_time,
                endTime=end_time,
                court_id=court_instance.court_Id,
                slot=int(slot_time)
            )


            return Response({
                "data": CourtMasterDetailSerializer(court_instance).data,  # serialized saved object
                "status": "success",
                "statusCode": status.HTTP_201_CREATED
            })
        else:
            
            return Response({
                "data": court_serializer.errors,
                "status": "failed",
                "statusCode": status.HTTP_400_BAD_REQUEST
            })
            
            
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        is_user_admin = UserMaster.objects.filter(reg_id=user.reg_id, user_type__id=2).exists()
        if not is_user_admin:
            return Response({
                "data": "User not valid or not admin",
                "status": "failed",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            })

        courts = CourtMaster.objects.filter(user=user.reg_id)

        if courts.exists():
            serializer = CourtMasterDetailSerializer(courts, many=True) 
            exclude_fields = ['flag', 'court_Id', 'user',"url",'court_Count']
            fields = []
            for field in CourtMaster._meta.get_fields():
                if field.many_to_one and field.auto_created:
                    continue
                if field.one_to_many:
                    continue
                if field.name in exclude_fields:
                    continue

                fields.append(field.name)
            return Response({
                "data": serializer.data,
                "fields":fields,
                "status": "Success",
                "statusCode": status.HTTP_200_OK
            })
        else:
            return Response({
                "data": [],
                "status": "failed",
                "statusCode": status.HTTP_404_NOT_FOUND
            })
            
    def put(self , request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        is_user_admin = UserMaster.objects.filter(reg_id=user.reg_id, user_type__id=2).exists()
        if not is_user_admin:
            return Response({
                "data": "User not valid or not admin",
                "status": "failed",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            }) 
            
        court_id = request.data.get("court_Id")
        if not court_id:
            return Response({
                "data":"Court Id require to update",
                "status":"failed",
                "statusCode":status.HTTP_200_OK,
            })
            
        
        court_data = CourtMaster.objects.get(court_Id = court_id)
        serilaized_data = CourtMasterDetailSerializer(court_data , data = request.data , partial=True)
        if serilaized_data.is_valid():
            serilaized_data.save()
            return Response({
                "data":serilaized_data.data,
                "status":"success",
                "statusCode":status.HTTP_200_OK
            })
        
            
            
        return Response({
            "data":f"invalied data { serilaized_data.error_messages}",
            "status":"failed",
            "statusCode":status.HTTP_400_BAD_REQUEST
        })
    
    def delete(self , request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        is_user_admin = UserMaster.objects.filter(reg_id=user.reg_id, user_type__id=2).exists()
        if not is_user_admin:
            return Response({
                "data": "User not valid or not admin",
                "status": "failed",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            }) 
        
        id = request.data.get("court_id")
        CourtMaster.objects.filter(court_Id = id).delete()
        return Response({
            "data":"Data has deleted",
            "status":"success",
            "statusCode":status.HTTP_200_OK
        })



class AdminSlotView(APIView):
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        is_user_admin = UserMaster.objects.filter(reg_id=user.reg_id, user_type__id=2).exists()
        if not is_user_admin:
            return Response({
                "data": "User not valid or not admin",
                "status": "failed",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            })
        court_id = request.query_params.get('court_id', None)
        if court_id is None:
                return Response({
                "status": "failed",
                "statusCode": status.HTTP_404_NOT_FOUND,
                "data": "Court No Required"
            })
        slot = SlotMaster.objects.filter(court__court_Id = court_id)
        serialized_data = SlotMasterSerializer(slot , many=True)
        return Response({
                "data": serialized_data.data,
                "status": "success",
                "statusCode": status.HTTP_200_OK
            }) 
    
    def put(self , request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        is_user_admin = UserMaster.objects.filter(reg_id=user.reg_id, user_type__id=2).exists()
        if not is_user_admin:
            return Response({
                "data": "User not valid or not admin",
                "status": "failed",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            }) 
            
        slots = request.data.get("slots" , [])
        for slot in slots:
            court_slot =slot["slot_Id"]
            slot_instance = SlotMaster.objects.get(slot_Id = court_slot)
            serialized = SlotMasterSerializer(slot_instance , data = slot , partial = True)
            if serialized.is_valid():
                serialized.save()
            
            
        return Response({
        "data": "Slots updated successfully",
        "status": "success",
        "statusCode": status.HTTP_200_OK
    }, status=status.HTTP_200_OK)

class AdminCourtHolidayView(APIView):
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        is_user_admin = UserMaster.objects.filter(reg_id=user.reg_id, user_type__id=2).exists()
        if not is_user_admin:
            return Response({
                "data": "User not valid or not admin",
                "status": "failed",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            })
            
        court_id = request.query_params.get("court_id" , None);
        if court_id is None : 
            return Response({
                "data":"court_id has required One !",
                "status":"failed",
                "statusCode":status.HTTP_400_BAD_REQUEST
            })
        Court = CourtMaster.objects.get(court_Id = court_id)
        holidays = HolidayMaster.objects.filter(court = Court)
        if holidays is not None :
            return Response({
                "status":"sucess",
                "statusCode":status.HTTP_200_OK
                ,"data":HolidayMasterSerializer(holidays , many=True).data
            })
            
    def post(self, request, *args, **kwargs):
       
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        is_user_admin = UserMaster.objects.filter(reg_id=user.reg_id, user_type__id=2).exists()
        if not is_user_admin:
            return Response({
                "data": "User not valid or not admin",
                "status": "failed",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            })
            
        court_id = request.data.get("court_id" , None)
        date = request.data.get("date" , None)
        isTournament = request.data.get("isTournament") 
        remark = request.data.get("remark")
        if court_id is not None and date is not None :
            court = CourtMaster.objects.get(court_Id = court_id)
            if court is None:
                return Response({
                    "data":"Court Id Not Available",
                    "status":"failed",
                    "statusCode":status.HTTP_400_BAD_REQUEST
                })
            holiday = HolidayMaster.objects.create(
                court = court,
                holiday_date = date,
                isTournament = isTournament,
                Remarks = remark,
                location_id = court.location
            )
            
            return Response({
                "data":HolidayMasterSerializer(holiday).data,
                "status":"success",
                "statusCode":status.HTTP_200_OK
            })

      
            
        
            
        
    
class AdminCourtBookedSlotsCheck(APIView):
    def get(self, request):
        user, error_response = get_user_from_token(request)
        if error_response:
            return error_response

        is_user_admin = UserMaster.objects.filter(reg_id=user.reg_id, user_type__id=2).exists()
        if not is_user_admin:
            return Response({
                "data": "User not valid or not admin",
                "status": "failed",
                "statusCode": status.HTTP_401_UNAUTHORIZED
            })
            
            
        court_id = request.query_params.get("court_id" , None);
        date = request.query_params.get("date" , None);
        if court_id is not None and date is not None:
            BookedSlots = BookingMaster.objects.filter(court__court_Id = court_id ,book_Date=date )
            return Response({
                "status":"success",
                "statusCode":status.HTTP_200_OK,
                "data":BookingMasterWithAllDataSerializer(BookedSlots , many=True).data
            })
                
        