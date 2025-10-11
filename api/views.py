from django.shortcuts import render
# from rest_framework import serializers, viewsets  
from rest_framework.decorators import api_view ,APIView
from rest_framework.response import Response
from api.utils import create_user_tokens,get_user_from_token
from .models import UserMaster 
from .serializers import  UserSerializer
from rest_framework import status

class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        mobile = request.data.get("mobile")

        if not mobile:
            return Response({
                "data": "Mobile number is required",
                "status": "error",
                "statusCode": status.HTTP_400_BAD_REQUEST
            })

        try:
            # Try to find existing user by mobile
            user = UserMaster.objects.get(mobile=mobile)
            print(user.mobile)
            serialized_data = UserSerializer(user)  # ✅ FIXED (removed many=True)
            token = create_user_tokens(user)

            return Response({
                "data": "User logged in successfully",
                "access": token,
                "user": serialized_data.data,
                "status": status.HTTP_200_OK
            })

        except UserMaster.DoesNotExist:
            # If user doesn't exist, validate and create new one
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                serialized_data = UserSerializer(user)  # ✅ FIXED here too
                print(user.mobile)
                token = create_user_tokens(user)

                return Response({
                    "data": "User created successfully",
                    "access": token,
                    "user": serialized_data.data,
                    "status": status.HTTP_201_CREATED
                })
            else:
                return Response({
                    "data": "Invalid form data",
                    "status": "error",
                    "errors": user_serializer.errors,
                    "statusCode": status.HTTP_400_BAD_REQUEST
                })


# @authentication_classes([CustomJWTAuthentication])
# @permission_classes([IsAuthenticated])
# class SportsCategoryView(APIView):
   
#      def get(self, request):
#         user, error_response = get_user_from_token(request)
#         if error_response:
#             return error_response
        
#         categories = SportCategory.objects.all()
#         serialized_data = SportsCategorySerializer(categories, many=True)
#         return Response({
#             "data": serialized_data.data,
#             "status": "success",
#             "statusCode": status.HTTP_200_OK
#         })
    


