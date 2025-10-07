from django.db import models
from django.utils import timezone
from api.models import UserMaster,SportCategory

# Assuming you have a Location model
class Sport(models.Model):
    sport_Id = models.AutoField(primary_key=True, db_column='sport_Id')
    category = models.ForeignKey(
        SportCategory, 
        db_column='name', 
        to_field='category_id',   # explicit reference to the correct PK
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'sport_Master'

    def __str__(self):
        return str(self.category)

class LocationMaster(models.Model):
    location_Id = models.AutoField(primary_key=True, db_column='location_Id')
    street = models.CharField(max_length=255, db_column='street', blank=True, null=True)
    mobile = models.CharField(max_length=20, db_column='mobile', blank=True, null=True)
    city = models.CharField(max_length=100, db_column='city', blank=True, null=True)
    state = models.CharField(max_length=100, db_column='state', blank=True, null=True)
    pincode = models.CharField(max_length=10, db_column='pincode', blank=True, null=True)
    flag = models.BooleanField(default=True, db_column='flag')
    name = models.CharField(max_length=255, db_column='name')

    # Foreign Keys
    sport = models.ForeignKey(Sport, on_delete=models.SET_NULL, null=True, blank=True, db_column='sport_Id')
    reg_Id = models.IntegerField(db_column='reg_Id', blank=True, null=True)
    merchantid = models.CharField(max_length=255, db_column='merchantid', blank=True, null=True)
    upi = models.CharField(max_length=255, db_column='upi', blank=True, null=True)
    convenience_Fees = models.FloatField(default=0, db_column='convenience_Fees')

    # Self-referential for group location
    grpLocation = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, db_column='grpLocation_Id')

    class Meta:
        db_table = 'location_Master'

    def __str__(self):
        return self.name
    
    
class CourtMaster(models.Model):
    court_Id = models.AutoField(primary_key=True, db_column='court_Id')
    court_Name = models.CharField(max_length=255, db_column='court_Name')
    court_Count = models.IntegerField(default=0, db_column='court_Count')
    coach_Count = models.IntegerField(default=0, db_column='coach_Count')
    url = models.URLField(max_length=500, blank=True, null=True, db_column='url')
    duration = models.IntegerField(help_text="Duration in minutes", db_column='duration')
    starttime = models.TimeField(db_column='starttime')
    endtime = models.TimeField(db_column='endtime')
    peakhours = models.IntegerField(default=0, db_column='peakhours')
    nonpeakhours = models.IntegerField(default=0, db_column='nonpeakhours')

    # Foreign keys
    location = models.ForeignKey('LocationMaster', on_delete=models.CASCADE, db_column='location_Id')
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE, db_column='user_Id')

    flag = models.BooleanField(default=True, db_column='flag')

    class Meta:
        db_table = 'court_Master'

    def __str__(self):
        return self.court_Name

# Assuming CourtMaster model is already defined
class SlotMaster(models.Model):
    slot_Id = models.AutoField(primary_key=True, db_column='slot_Id')
    court = models.ForeignKey('CourtMaster', on_delete=models.CASCADE, db_column='court_Id')
    slot_Name = models.CharField(max_length=255, db_column='slot_Name')
    IsPeak = models.BooleanField(default=False, db_column='IsPeak')
    IsActive = models.BooleanField(default=True, db_column='IsActive')

    # Days of the week
    Mon = models.BooleanField(default=False, db_column='Mon')
    Tue = models.BooleanField(default=False, db_column='Tue')
    Wed = models.BooleanField(default=False, db_column='Wed')
    Thu = models.BooleanField(default=False, db_column='Thu')
    Fri = models.BooleanField(default=False, db_column='Fri')
    Sat = models.BooleanField(default=False, db_column='Sat')
    Sun = models.BooleanField(default=False, db_column='Sun')

    # Audit fields
    created_By = models.ForeignKey(UserMaster, on_delete=models.SET_NULL, null=True, blank=True, related_name='slot_created_by', db_column='created_By')
    created_Date = models.DateTimeField(auto_now=True, db_column='created_Date')
    updated_By = models.ForeignKey(UserMaster, on_delete=models.SET_NULL, null=True, blank=True, related_name='slot_updated_by', db_column='updated_By')
    updated_Date = models.DateTimeField(auto_now=True, db_column='updated_Date')

    class Meta:
        db_table = 'slot_Master'

    def __str__(self):
        return self.slot_Name


class BookingMaster(models.Model):
    book_Id = models.AutoField(primary_key=True, db_column='book_Id')
    book_Date = models.DateField(db_column='book_Date')

    # Foreign Keys
    slot = models.ForeignKey('SlotMaster', on_delete=models.CASCADE, db_column='slot_Id')
    court = models.ForeignKey('CourtMaster', on_delete=models.CASCADE, db_column='court_Id')
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE, null=True, blank=True, db_column='mobile')  # assuming mobile maps to User

    # Slot info (optional redundancy)
    slot_Name = models.CharField(max_length=255, db_column='slot_Name', blank=True, null=True)

    # Payment & amount
    reg_Id = models.IntegerField(db_column='reg_Id', blank=True, null=True)
    discount = models.FloatField(default=0, db_column='discount')
    discount_Amt = models.FloatField(default=0, db_column='discount_Amt')
    actual_Amt = models.FloatField(default=0, db_column='actual_Amt')
    final_Amt = models.FloatField(default=0, db_column='final_Amt')
    payment_Id = models.CharField(max_length=255, blank=True, null=True, db_column='payment_Id')

    flag = models.BooleanField(default=True, db_column='flag')

    # Audit fields
    created_Date = models.DateTimeField(auto_now=True, db_column='created_Date')
    modified_By = models.ForeignKey(UserMaster, on_delete=models.SET_NULL, null=True, blank=True, related_name='booking_modified_by', db_column='modified_By')
    modified_Date = models.DateTimeField(auto_now=True, db_column='modified_Date')

    class Meta:
        db_table = 'booking_Master'

    def __str__(self):
        return f'Booking {self.book_Id} - {self.slot_Name}'