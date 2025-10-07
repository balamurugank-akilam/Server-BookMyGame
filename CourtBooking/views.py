from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import CourtMasterSerializer
from .models import CourtMaster
from rest_framework import status
from api.utils import get_user_from_token

# Create your views here.


class CourtView(APIView):
    
    def get(self , request , sport ):
        user , error_response = get_user_from_token(request)
        if error_response :
            return Response({
                "data":"Token expaired or Not Available",
                "status":"failed",
                "statusCode":status.HTTP_401_UNAUTHORIZED
            })
        data = CourtMaster.objects.all()
        courtMaster_serialized = CourtMasterSerializer(data ,many = True)
        return Response({
            "data":courtMaster_serialized.data,
            "status":"Success",
            "statusCode":status.HTTP_200_OK
        })