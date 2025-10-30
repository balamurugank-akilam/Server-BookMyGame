from rest_framework import serializers
from .models import SportCategory, SportMaster, LocationMaster, CourtMaster, SlotMaster, BookingMaster , CourtType,SessionMaster
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




# Nested serializers for detailed views
class SportMasterDetailSerializer(serializers.ModelSerializer):
    category = SportCategorySerializer(read_only=True)
    
    class Meta:
        model = SportMaster
        fields = '__all__'
        
        
#-----------------------------------------Location-------------------------------        
        
class LocationMasterSerializer(serializers.ModelSerializer):
    sport_name = serializers.CharField(source='sport.name', read_only=True)
    grpLocation_name = serializers.CharField(source='grpLocation.name', read_only=True)
    
    
    class Meta:
        model = LocationMaster
        fields = '__all__'
        extra_fields = ['sport_name', 'grpLocation_name']
        

class LocationMasterDetailSerializer(serializers.ModelSerializer):
    sport = SportMasterSerializer(read_only=True)
    sport_Id = serializers.PrimaryKeyRelatedField(
    queryset=SportMaster.objects.all(),
    source='sport',  # maps to model's sport field
    write_only=True
)
    
    
    class Meta:
        model = LocationMaster
        fields = '__all__'
        
        



class LocationWithCourtsSerializer(serializers.Serializer):
    venue = serializers.CharField(source='location.name')
    location_Id = serializers.IntegerField(source='location.location_Id', read_only=True)

    address = serializers.SerializerMethodField()
    contact = serializers.CharField(source='location.mobile')
    courts = serializers.SerializerMethodField()

    def get_address(self, obj):
        loc = obj.location
        return f"{loc.street}, {loc.city}, {loc.state} - {loc.pincode}"

    def get_courts(self, obj):
        courts = CourtMaster.objects.filter(location=obj.location, )
        return CourtListSerializer(courts, many=True).data




    

    
    
#-------------------------------CourtSerializers ------------------------------------------

class CourtTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtType
        fields = ['court_type_id', 'court_type']

class CourtMasterSerializer(serializers.ModelSerializer):
    location = LocationMasterSerializer()
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

class CourtMasterForBookedSlotSerializer(serializers.ModelSerializer):
    location = LocationMasterSerializer()
    user_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = CourtMaster
        fields = ['court_Id' , "court_Name","court_Count","coach_Count","url","flag","user_details","location"]
        extra_fields = ['location_name', 'user_details']
    
    def get_user_details(self, obj):
        if obj.user:
            return {
                'user_id': obj.user.reg_id,
                'mobile': obj.user.mobile,
                'name': obj.user.name
            }
        return None
        

class CourtMasterDetailSerializer(serializers.ModelSerializer):
    # show nested details when reading
    location = LocationMasterSerializer(read_only=True)
    # accept only the ID when writing
    location_Id = serializers.PrimaryKeyRelatedField(
        queryset=LocationMaster.objects.all(), 
        source='location',  # maps to the FK field in the model
        write_only=True
    )
   
    user = serializers.SerializerMethodField()
    court_type = CourtTypeSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset = UserMaster.objects.all(),
        source="user",
        write_only = True
    )
    court_type_Id = serializers.PrimaryKeyRelatedField(
        queryset = CourtType.objects.all(),
        source = "court_type",
        write_only = True
    )
    

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
    
    
    
   ###-----------------------------slot serializedrs ---------------------------------------- 
class SessionMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionMaster
        fields = ['session_Id', 'session_name']   # Use correct model field names




class SlotMasterSerializer(serializers.ModelSerializer):
    court_name = serializers.CharField(source='court.court_Name', read_only=True)
    # created_by_name = serializers.CharField(source='created_By.name', read_only=True)
    # updated_by_name = serializers.CharField(source='updated_By.name', read_only=True)
    session_name = serializers.CharField(source='session_Id.session_name', read_only=True)
    court_id = serializers.IntegerField(source = 'court.court_Id' , read_only = True)




    class Meta:
        model = SlotMaster
        # Explicitly list fields including extra fields
        fields = [
            'slot_Id', 'slot_Name', 'IsPeak', 'IsActive', 
            'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun',
            'created_By', 'created_Date', 'updated_By', 'updated_Date',
            'court_name', 'session_name' ,"court_id","IsMember"
        ]
        extra_fields =['session_name']
        
    def get_session_name(self, obj):
        return obj.session.session_name if obj.session else None


        
        

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
    
 
    
    # def get_user(self, obj):
    #     if obj.user:
    #         return {
    #             'user_id': obj.user.reg_id,
    #             'mobile': obj.user.mobile,
    #             'name': obj.user.name
    #         }
    #     return None
    
    # def get_modified_By(self, obj):
    #     if obj.modified_By:
    #         return {
    #             'user_id': obj.modified_By.reg_id,
    #             'mobile': obj.modified_By.mobile,
    #             'name': obj.modified_By.name
    #         }
    #     return None







#### bookiking serializers -------------------------------------------------------------



   #booked slott view using below
class BookedSlotViewSerializer(serializers.ModelSerializer):
    slot = SlotMasterSerializer(read_only=True)
    # court_Id = serializers.IntegerField(source = 'court.court_Id', read_only = True)
   
    
    class Meta:
        model = BookingMaster
        fields = ['slot' ]
        
        
        
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
                'user_id': obj.user.reg_id,
                'mobile': obj.user.mobile,
                'name': obj.user.name
            }
        return None
    
    
    
class BookingMasterDetailSerializer(serializers.ModelSerializer):
    slot = SlotMasterDetailSerializer(read_only=True)

    court = CourtMasterDetailSerializer(read_only=True)
    user = serializers.SerializerMethodField()
    modified_By = serializers.SerializerMethodField()
   
    
    class Meta:
        model = BookingMaster
        fields = '__all__'
    
    def get_user(self, obj):
        if obj.user:
            return {
                'user_id': obj.user.reg_id,
                'mobile': obj.user.mobile,
                'name': obj.user.name
            }
        return None
    
    def get_modified_By(self, obj):
        if obj.modified_By:
            return {
                'user_id': obj.modified_By.reg_id,
                'mobile': obj.modified_By.mobile,
                'name': obj.modified_By.name
            }
        return None
    
    
class BookingMasterWithAllDataSerializer(serializers.ModelSerializer):
    slot = serializers.SerializerMethodField()

    court = CourtMasterForBookedSlotSerializer()
    user = serializers.SerializerMethodField()
    modified_By = serializers.SerializerMethodField()
   
   
    
    class Meta:
        model = BookingMaster
        fields = '__all__'
    
    def get_user(self, obj):
        if obj.user:
            return {
                'user_id': obj.user.reg_id,
                'mobile': obj.user.mobile,
                'name': obj.user.name
            }
        return None
    
    def get_modified_By(self, obj):
        if obj.modified_By:
            return {
                'user_id': obj.modified_By.reg_id,
                'mobile': obj.modified_By.mobile,
                'name': obj.modified_By.name
            }
        return None
    
    def get_slot(self,obj):
        if obj.slot:
            return {
                "slot_Id":int(obj.slot.slot_Id),
                "slot_Name":str(obj.slot.slot_Name)
            }
            

    
class BookingMasterWriteSerializer(serializers.ModelSerializer):
    slot = serializers.DictField(write_only=True)
    court = serializers.DictField(write_only=True)
    user = serializers.DictField(write_only=True)

    class Meta:
        model = BookingMaster
        fields = [
            'book_Date', 'slot', 'court', 'user',
            'slot_Name', 'reg_Id', 'actual_Amt', 'discount_Amt'
        ]

    def validate(self, attrs):
        # Extract IDs from nested objects
        try:
            attrs['slot_id'] = attrs.pop('slot')['slot_Id']
            attrs['court_id'] = attrs.pop('court')['court_Id']
            attrs['user_id'] = attrs.pop('user')['reg_id']
        except KeyError:
            raise serializers.ValidationError(
                "Nested objects must include 'slot_Id', 'court_Id', and 'reg_id'."
            )

        # Check if slot is already booked
        book_date = attrs.get('book_Date')
        if BookingMaster.objects.filter(
            slot_id=attrs['slot_id'],
            court_id=attrs['court_id'],
            book_Date=book_date
        ).exists():
            raise serializers.ValidationError("Slot has already been booked.")

        return attrs

    def create(self, validated_data):
        # Remove nested objects (they have been mapped to *_id fields)
        validated_data.pop('slot', None)
        validated_data.pop('court', None)
        validated_data.pop('user', None)

        # Calculate final amount if discount is present
        actual = validated_data.get('actual_Amt', 0)
        discount = validated_data.get('discount_Amt', 0)
        validated_data['final_Amt'] = actual - discount

        return BookingMaster.objects.create(**validated_data)