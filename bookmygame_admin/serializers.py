from rest_framework import serializers
from .models import HolidayMaster,MembershipMaster
from CourtBooking.models import CourtMaster  ,SlotMaster
from CourtBooking.serializers import CourtMasterSerializer , LocationMasterSerializer 




class HolidayMasterSerializer(serializers.ModelSerializer):
    court_name = serializers.CharField(source='court.courtName', read_only=True)
    court_id = serializers.IntegerField(source = "court.court_Id" , read_only = True)
    location_id = serializers.IntegerField(source = "court.location.location_Id" , read_only = True)

    class Meta:
        model = HolidayMaster
        fields = [
            'holiday_Id',
            'holiday_date',
            'flag',
            'leave_Type',
            'location_id',
            'court_id',
            'court_name',
            'Remarks',
            "isTournament",
       
        ]



class MembershipMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipMaster
        fields = [
            'mem_Id',
            'mem_Name',
            'mem_Mobile',
            'mem_Fees',
            'mem_Proof',
            'mem_Password',
            'mem_paymentMode',
            'mem_Court',
            'mem_DOJ',
            'mem_PendingFee',
            'mem_Photo',
            'mem_Location',
            'memstart_Time',
            'memend_Time',
            'mem_Remarks',
            'active_Flag',
            'created_By',
            'created_Date',
            'modified_By',
            'modified_Date',
        ]
        read_only_fields = ['mem_Id', 'created_Date', 'modified_Date']
