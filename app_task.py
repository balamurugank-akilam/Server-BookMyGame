from datetime import datetime, timedelta, time

from celery import shared_task
from django.utils import timezone
from CourtBooking.models import BookingMaster , SlotMaster,CourtMaster ,SessionMaster

@shared_task
def release_expired_unpaid_holds():
    now = timezone.now()
    expired = BookingMaster.objects.filter(
        hold_expires_at__lt=now,
        payment_Id__isnull=True
    )
    count = expired.count()
    expired.update(flag=False, hold_expires_at=None, )
    print(f"Released {count} unpaid holds")



class CreateTimeslots:
    def __init__(self):
        self.delta = timedelta(minutes=30)
        today = datetime.today()
        self.morning = today.replace(hour=12, minute=0, second=0, microsecond=0)
        self.afternoon = today.replace(hour=17, minute=0, second=0, microsecond=0)

    def basicTimeslot(self, startTime, endTime, court_id , slot):
        today = datetime.today()
        self.delta = timedelta(minutes=slot)
        # Ensure startTime and endTime are datetime objects
        if isinstance(startTime, time):
            startTime = datetime.combine(today.date(), startTime)
        if isinstance(endTime, time):
            endTime = datetime.combine(today.date(), endTime)


        current_time = startTime
        court = CourtMaster.objects.get(court_Id=court_id)
        session_id = 1
        
        while current_time <= endTime:
            if current_time < self.morning:
                session_id = 1
              
            elif current_time < self.afternoon:
                session_id = 2
            else:
              
                session_id = 3
                
            session = SessionMaster.objects.get(session_Id = session_id)
            slot_name = current_time.strftime("%H:%M")

            SlotMaster.objects.create(
                court=court,
                slot_Name=slot_name,
                session_Id=session,
               
            )

            current_time += self.delta
