from django.shortcuts import render
from api.utils import get_user_from_token
from rest_framework.decorators import APIView
from rest_framework.response import Response
from api.models import UserMaster , UserTypeMaster
from CourtBooking.models import LocationMaster
from CourtBooking.serializers import LocationMasterDetailSerializer
from rest_framework import status

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
            serialzer_data.save()
            
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
    
        

