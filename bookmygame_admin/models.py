from django.db import models
from CourtBooking.models import CourtMaster

# Create your models here.
class HolidayMaster(models.Model):
    holiday_Id = models.AutoField(db_column='holiday_Id', primary_key=True)
    holiday_date = models.DateField(db_column='holiday_date')
    flag = models.BooleanField(db_column='flag', default=False)
    leave_Type = models.CharField(db_column='leave_Type', max_length=100, null=True, blank=True)
    location_id = models.IntegerField(db_column='location_id', null=True, blank=True)

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