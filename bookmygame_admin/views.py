from django.shortcuts import render
from api.utils import get_user_from_token
from rest_framework.decorators import APIView
from rest_framework.response import Response
from api.models import UserMaster , UserTypeMaster 
from CourtBooking.models import CourtMaster
from CourtBooking.models import LocationMaster
from CourtBooking.serializers import LocationMasterDetailSerializer , CourtMasterDetailSerializer
from rest_framework import status
from django.apps import apps
from app_task import CreateTimeslots

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



# class SlotView(APIView):
    
        

