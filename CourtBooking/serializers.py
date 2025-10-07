from rest_framework import serializers
from .models import Sport, LocationMaster, CourtMaster, SlotMaster, BookingMaster
from api.models import UserMaster, SportCategory

class SportCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SportCategory
        fields = ['category_id', 'name']  # Adjust fields based on your actual SportCategory model

class SportSerializer(serializers.ModelSerializer):
    category = SportCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SportCategory.objects.all(), 
        source='category', 
        write_only=True
    )
    
    class Meta:
        model = Sport
        fields = ['sport_Id', 'category', 'category_id']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # You can customize the representation if needed
        return representation

class LocationMasterSerializer(serializers.ModelSerializer):
    sport = SportSerializer(read_only=True)
    sport_Id = serializers.PrimaryKeyRelatedField(
        queryset=Sport.objects.all(), 
        source='sport', 
        write_only=True, 
        required=False, 
        allow_null=True
    )
    
    grpLocation = serializers.StringRelatedField(read_only=True)
    grpLocation_Id = serializers.PrimaryKeyRelatedField(
        queryset=LocationMaster.objects.all(), 
        source='grpLocation', 
        write_only=True, 
        required=False, 
        allow_null=True
    )
    
    class Meta:
        model = LocationMaster
        fields = [
            'location_Id', 'street', 'mobile', 'city', 'state', 'pincode', 
            'flag', 'name', 'sport', 'sport_Id', 'reg_Id', 'merchantid', 
            'upi', 'convenience_Fees', 'grpLocation', 'grpLocation_Id'
        ]
        read_only_fields = ['location_Id']

class CourtMasterSerializer(serializers.ModelSerializer):
    location = LocationMasterSerializer(read_only=True)
    location_Id = serializers.PrimaryKeyRelatedField(
        queryset=LocationMaster.objects.all(), 
        source='location', 
        write_only=True
    )
    
    user = serializers.StringRelatedField(read_only=True)
    user_Id = serializers.PrimaryKeyRelatedField(
        queryset=UserMaster.objects.all(), 
        source='user', 
        write_only=True
    )
    
    class Meta:
        model = CourtMaster
        fields = [
            'court_Id', 'court_Name', 'court_Count', 'coach_Count', 'url',
            'duration', 'starttime', 'endtime', 'peakhours', 'nonpeakhours',
            'location', 'location_Id', 'user', 'user_Id', 'flag'
        ]
        read_only_fields = ['court_Id']

class SlotMasterSerializer(serializers.ModelSerializer):
    court = CourtMasterSerializer(read_only=True)
    court_Id = serializers.PrimaryKeyRelatedField(
        queryset=CourtMaster.objects.all(), 
        source='court', 
        write_only=True
    )
    
    created_By = serializers.StringRelatedField(read_only=True)
    updated_By = serializers.StringRelatedField(read_only=True)
    
    created_By_Id = serializers.PrimaryKeyRelatedField(
        queryset=UserMaster.objects.all(), 
        source='created_By', 
        write_only=True, 
        required=False, 
        allow_null=True
    )
    
    updated_By_Id = serializers.PrimaryKeyRelatedField(
        queryset=UserMaster.objects.all(), 
        source='updated_By', 
        write_only=True, 
        required=False, 
        allow_null=True
    )
    
    days_of_week = serializers.SerializerMethodField()
    
    class Meta:
        model = SlotMaster
        fields = [
            'slot_Id', 'court', 'court_Id', 'slot_Name', 'IsPeak', 'IsActive',
            'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'days_of_week',
            'created_By', 'created_By_Id', 'created_Date', 'updated_By', 
            'updated_By_Id', 'updated_Date'
        ]
        read_only_fields = ['slot_Id', 'created_Date', 'updated_Date']
    
    def get_days_of_week(self, obj):
        """Returns list of active days"""
        days = []
        if obj.Mon: days.append('Monday')
        if obj.Tue: days.append('Tuesday')
        if obj.Wed: days.append('Wednesday')
        if obj.Thu: days.append('Thursday')
        if obj.Fri: days.append('Friday')
        if obj.Sat: days.append('Saturday')
        if obj.Sun: days.append('Sunday')
        return days

class BookingMasterSerializer(serializers.ModelSerializer):
    slot = SlotMasterSerializer(read_only=True)
    slot_Id = serializers.PrimaryKeyRelatedField(
        queryset=SlotMaster.objects.all(), 
        source='slot', 
        write_only=True
    )
    
    court = CourtMasterSerializer(read_only=True)
    court_Id = serializers.PrimaryKeyRelatedField(
        queryset=CourtMaster.objects.all(), 
        source='court', 
        write_only=True
    )
    
    user = serializers.StringRelatedField(read_only=True)
    mobile = serializers.PrimaryKeyRelatedField(
        queryset=UserMaster.objects.all(), 
        source='user', 
        write_only=True, 
        required=False, 
        allow_null=True
    )
    
    modified_By = serializers.StringRelatedField(read_only=True)
    modified_By_Id = serializers.PrimaryKeyRelatedField(
        queryset=UserMaster.objects.all(), 
        source='modified_By', 
        write_only=True, 
        required=False, 
        allow_null=True
    )
    
    # Calculated fields
    total_discount = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    
    class Meta:
        model = BookingMaster
        fields = [
            'book_Id', 'book_Date', 'slot', 'slot_Id', 'court', 'court_Id',
            'user', 'mobile', 'slot_Name', 'reg_Id', 'discount', 'discount_Amt',
            'actual_Amt', 'final_Amt', 'payment_Id', 'flag', 'created_Date',
            'modified_By', 'modified_By_Id', 'modified_Date', 'total_discount',
            'payment_status'
        ]
        read_only_fields = ['book_Id', 'created_Date', 'modified_Date']
    
    def get_total_discount(self, obj):
        """Calculate total discount percentage"""
        if obj.actual_Amt > 0:
            return (obj.discount_Amt / obj.actual_Amt) * 100
        return 0
    
    def get_payment_status(self, obj):
        """Determine payment status based on payment_Id"""
        return "Paid" if obj.payment_Id else "Pending"
    
    def validate(self, data):
        """Custom validation for booking"""
        # Ensure booking date is not in the past
        if data.get('book_Date') and data['book_Date'] < timezone.now().date():
            raise serializers.ValidationError("Booking date cannot be in the past")
        
        # Ensure final amount calculation is correct
        if data.get('actual_Amt') and data.get('discount_Amt'):
            calculated_final_amt = data['actual_Amt'] - data['discount_Amt']
            if data.get('final_Amt') != calculated_final_amt:
                raise serializers.ValidationError("Final amount calculation is incorrect")
        
        return data

# Nested serializers for detailed views
class CourtDetailSerializer(CourtMasterSerializer):
    """Extended Court serializer with slots"""
    slots = SlotMasterSerializer(many=True, read_only=True, source='slotmaster_set')
    
    class Meta(CourtMasterSerializer.Meta):
        fields = CourtMasterSerializer.Meta.fields + ['slots']

class LocationDetailSerializer(LocationMasterSerializer):
    """Extended Location serializer with courts"""
    courts = CourtMasterSerializer(many=True, read_only=True, source='courtmaster_set')
    
    class Meta(LocationMasterSerializer.Meta):
        fields = LocationMasterSerializer.Meta.fields + ['courts']

class SlotDetailSerializer(SlotMasterSerializer):
    """Extended Slot serializer with bookings"""
    bookings = BookingMasterSerializer(many=True, read_only=True, source='bookingmaster_set')
    
    class Meta(SlotMasterSerializer.Meta):
        fields = SlotMasterSerializer.Meta.fields + ['bookings']