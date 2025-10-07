from rest_framework import serializers
from .models import SportCategory , UserTypeMaster , UserMaster

class SportsCategorySerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    class Meta:
        model = SportCategory
        fields = "__all__"
        
    # def get_image(self, obj):
    #     request = self.context.get('request')
    #     if obj.image and hasattr(obj.image, 'url'):
    #         return request.build_absolute_uri(obj.image.url)
    #     return None
  
class UserTypeSerializer(serializers.ModelSerializer):
    class Meta :
        model = UserTypeMaster
        fields = "__all__"  
    
class UserSerializer(serializers.ModelSerializer):
    
    class Meta :
        model = UserMaster
        fields = "__all__"