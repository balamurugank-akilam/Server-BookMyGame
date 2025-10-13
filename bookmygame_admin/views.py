from django.shortcuts import render
from api.utils import get_user_from_token
from rest_framework.decorators import APIView
from rest_framework.response import Response
from api.models import UserMaster , UserTypeMaster
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

        

