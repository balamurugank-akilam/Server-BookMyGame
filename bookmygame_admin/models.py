from django.db import models
from CourtBooking.models import CourtMaster  , LocationMaster

# Create your models here.
class HolidayMaster(models.Model):
    holiday_Id = models.AutoField(db_column='holiday_Id', primary_key=True)
    holiday_date = models.DateField(db_column='holiday_date')
    flag = models.BooleanField(db_column='flag', default=False)
    leave_Type = models.CharField(db_column='leave_Type', max_length=100, null=True, blank=True)
    location_id = models.ForeignKey(LocationMaster , on_delete=models.CASCADE ,db_column='location_id', null=True, blank=True)
    isTournament = models.BooleanField(db_column="isTournament",default=False)
    # Foreign key relation
    court = models.ForeignKey(
        CourtMaster,
        db_column='court_id',
        on_delete=models.CASCADE,
        related_name='holidays',
        
    )

    Remarks = models.TextField(db_column='Remarks', null=True, blank=True)

    class Meta:
        db_table = 'holiday_Master'
        verbose_name = 'Holiday Master'
        verbose_name_plural = 'Holiday Masters'

    def __str__(self):
        return f"{self.holiday_date} - {self.leave_Type}"
    



class MembershipMaster(models.Model):
    mem_Id = models.AutoField(primary_key=True, db_column='mem_Id')
    mem_Name = models.CharField(max_length=255, db_column='mem_Name')
    mem_Mobile = models.CharField(max_length=15, db_column='mem_Mobile')
    mem_Fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='mem_Fees')
    mem_Proof = models.CharField(max_length=255, null=True, blank=True, db_column='mem_Proof')
    mem_Password = models.CharField(max_length=255, db_column='mem_Password')
    mem_paymentMode = models.CharField(max_length=50, null=True, blank=True, db_column='mem_paymentMode')
    mem_Court = models.CharField(max_length=255, null=True, blank=True, db_column='mem_Court')
    mem_DOJ = models.DateField(null=True, blank=True, db_column='mem_DOJ')
    mem_PendingFee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='mem_PendingFee')
    mem_Photo = models.ImageField(upload_to='member_photos/', null=True, blank=True, db_column='mem_Photo')
    mem_Location = models.CharField(max_length=255, null=True, blank=True, db_column='mem_Location')
    memstart_Time = models.TimeField(null=True, blank=True, db_column='memstart_Time')
    memend_Time = models.TimeField(null=True, blank=True, db_column='memend_Time')
    mem_Remarks = models.TextField(null=True, blank=True, db_column='mem_Remarks')
    active_Flag = models.BooleanField(default=True, db_column='active_Flag')
    created_By = models.CharField(max_length=255, null=True, blank=True, db_column='created_By')
    created_Date = models.DateTimeField(auto_now_add=True, db_column='created_Date')
    modified_By = models.CharField(max_length=255, null=True, blank=True, db_column='modified_By')
    modified_Date = models.DateTimeField(auto_now=True, db_column='modified_Date')

    class Meta:
        db_table = 'membership_Master'
        verbose_name = 'Membership Master'
        verbose_name_plural = 'Membership Masters'

    def __str__(self):
        return f"{self.mem_Name} ({self.mem_Mobile})"
