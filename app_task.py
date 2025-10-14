from celery import shared_task
from django.utils import timezone
from CourtBooking.models import BookingMaster

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
