from rest_framework import serializers
from .models import HolidayMaster
from CourtBooking.models import CourtMaster
from CourtBooking.serializers import CourtMasterSerializer , LocationMasterSerializer


class HolidayMasterSerializer(serializers.ModelSerializer):
    court_name = serializers.CharField(source='court.courtName', read_only=True)
    court_id = serializers.IntegerField(source = "court.court_Id" , read_only = True)
    location_id = LocationMasterSerializer(read_only = True)

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
