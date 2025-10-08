from django.shortcuts import render
from rest_framework.decorators import APIView,api_view
from rest_framework.response import Response
from .serializers import CourtMasterSerializer, LocationWithCourtsSerializer , SportMasterSerializer,CourtMasterDetailSerializer
from .models import CourtMaster
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
                    
                return Response({
                     "status": "success",
                     "statusCode": 200,
                     "data":serializer.data,
                   
                    })
