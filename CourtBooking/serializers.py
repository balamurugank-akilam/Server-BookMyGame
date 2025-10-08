from rest_framework import serializers
from .models import SportCategory, SportMaster, LocationMaster, CourtMaster, SlotMaster, BookingMaster , CourtType
from api.models import UserMaster

class SportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SportCategory
        fields = '__all__'

class SportMasterSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = SportMaster
        fields = '__all__'
        extra_fields = ['category_name']

class LocationMasterSerializer(serializers.ModelSerializer):
    sport_name = serializers.CharField(source='sport.name', read_only=True)
    grpLocation_name = serializers.CharField(source='grpLocation.name', read_only=True)
    
    class Meta:
        model = LocationMaster
        fields = '__all__'
        extra_fields = ['sport_name', 'grpLocation_name']
        
class CourtTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtType
        fields = ['court_type_id', 'court_type']

class CourtMasterSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    user_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = CourtMaster
        fields = '__all__'
        extra_fields = ['location_name', 'user_details']
    
    def get_user_details(self, obj):
        if obj.user:
            return {
                'user_id': obj.user.reg_id,
                'mobile': obj.user.mobile,
                'name': obj.user.name
            }
        return None

class SlotMasterSerializer(serializers.ModelSerializer):
    court_name = serializers.CharField(source='court.court_Name', read_only=True)
    created_by_name = serializers.CharField(source='created_By.name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_By.name', read_only=True)
    
    class Meta:
        model = SlotMaster
        fields = '__all__'
        extra_fields = ['court_name', 'created_by_name', 'updated_by_name']

class BookingMasterSerializer(serializers.ModelSerializer):
    slot_details = serializers.SerializerMethodField(read_only=True)
    court_details = serializers.SerializerMethodField(read_only=True)
    user_details = serializers.SerializerMethodField(read_only=True)
    modified_by_name = serializers.CharField(source='modified_By.name', read_only=True)
    
    class Meta:
        model = BookingMaster
        fields = '__all__'
        extra_fields = ['slot_details', 'court_details', 'user_details', 'modified_by_name']
    
    def get_slot_details(self, obj):
        if obj.slot:
            return {
                'slot_id': obj.slot.slot_Id,
                'slot_name': obj.slot.slot_Name,
                'is_peak': obj.slot.IsPeak
            }
        return None
    
    def get_court_details(self, obj):
        if obj.court:
            return {
                'court_id': obj.court.court_Id,
                'court_name': obj.court.court_Name,
                'location_id': obj.court.location.location_Id if obj.court.location else None,
                'location_name': obj.court.location.name if obj.court.location else None
            }
        return None
    
    def get_user_details(self, obj):
        if obj.user:
            return {
                'user_id': obj.user.user_id,
                'mobile': obj.user.mobile,
                'name': obj.user.name
            }
        return None

# Nested serializers for detailed views
class SportMasterDetailSerializer(serializers.ModelSerializer):
    category = SportCategorySerializer(read_only=True)
    
    class Meta:
        model = SportMaster
        fields = '__all__'

class LocationMasterDetailSerializer(serializers.ModelSerializer):
    sport = SportMasterSerializer(read_only=True)
    grpLocation = LocationMasterSerializer(read_only=True)
    
    class Meta:
        model = LocationMaster
        fields = '__all__'

class CourtMasterDetailSerializer(serializers.ModelSerializer):
    location = LocationMasterSerializer(read_only=True)
    user = serializers.SerializerMethodField()
    court_type = CourtTypeSerializer()
    
    class Meta:
        model = CourtMaster
        fields = '__all__'
    
    def get_user(self, obj):
        if obj.user:
            return {
                'user_id': obj.user.reg_id,
                'mobile': obj.user.mobile,
                'name': obj.user.name
            }
        return None

class SlotMasterDetailSerializer(serializers.ModelSerializer):
    court = CourtMasterSerializer(read_only=True)
    created_By = serializers.SerializerMethodField()
    updated_By = serializers.SerializerMethodField()
    
    class Meta:
        model = SlotMaster
        fields = '__all__'
    
    def get_created_By(self, obj):
        if obj.created_By:
            return {
                'user_id': obj.created_By.user_id,
                'mobile': obj.created_By.mobile,
                'name': obj.created_By.name
            }
        return None
    
    def get_updated_By(self, obj):
        if obj.updated_By:
            return {
                'user_id': obj.updated_By.user_id,
                'mobile': obj.updated_By.mobile,
                'name': obj.updated_By.name
            }
        return None

class BookingMasterDetailSerializer(serializers.ModelSerializer):
    slot = SlotMasterSerializer(read_only=True)
    court = CourtMasterSerializer(read_only=True)
    user = serializers.SerializerMethodField()
    modified_By = serializers.SerializerMethodField()
    
    class Meta:
        model = BookingMaster
        fields = '__all__'
    
    def get_user(self, obj):
        if obj.user:
            return {
                'user_id': obj.user.user_id,
                'mobile': obj.user.mobile,
                'name': obj.user.name
            }
        return None
    
    def get_modified_By(self, obj):
        if obj.modified_By:
            return {
                'user_id': obj.modified_By.user_id,
                'mobile': obj.modified_By.mobile,
                'name': obj.modified_By.name
            }
        return None


class CourtListSerializer(serializers.ModelSerializer):
    court_type = serializers.CharField(source='court_type.court_type')
    timings = serializers.SerializerMethodField()

    class Meta:
        model = CourtMaster
        fields = [
            'court_Id', 'court_type', 'court_Name', 'court_Count',
            'peakhours', 'nonpeakhours', 'ratings', 'timings'
        ]

    def get_timings(self, obj):
        start = obj.starttime[:5]  # "HH:MM:SS" -> "HH:MM"
        end = obj.endtime[:5]
        return f"{start} - {end}"


class LocationWithCourtsSerializer(serializers.Serializer):
    venue = serializers.CharField(source='location.name')
    address = serializers.SerializerMethodField()
    contact = serializers.CharField(source='location.mobile')
    courts = serializers.SerializerMethodField()

    def get_address(self, obj):
        loc = obj.location
        return f"{loc.street}, {loc.city}, {loc.state} - {loc.pincode}"

    def get_courts(self, obj):
        courts = CourtMaster.objects.filter(location=obj.location, flag=True)
        return CourtListSerializer(courts, many=True).data




    

    
    
