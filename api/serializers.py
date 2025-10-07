from rest_framework import serializers
from .models import  UserTypeMaster , UserMaster


  
class UserTypeSerializer(serializers.ModelSerializer):
    class Meta :
        model = UserTypeMaster
        fields = "__all__"  
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = UserMaster
        fields = "__all__"