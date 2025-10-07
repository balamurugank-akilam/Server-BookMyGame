from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .serializers import CourtMasterSerializer , SportMasterSerializer,CourtMasterDetailSerializer
from .models import CourtMaster
from rest_framework import status
from api.utils import get_user_from_token
from .models import SportMaster

# Create your views here.


class CourtView(APIView , ):
    
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
            
       
            
        data = CourtMaster.objects.all()
        courtMaster_serialized = CourtMasterSerializer(data ,many = True)
        return Response({
            "data":courtMaster_serialized.data,
            "status":"Success",
            "statusCode":status.HTTP_200_OK
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