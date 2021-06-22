from game.models import SuspendDate
from datetime import timedelta

from django.utils import timezone

def one_month_from_today():
    return timezone.now() + timedelta(days=30)

def run():
    s = SuspendDate.objects.first()
    s.suspend_date = one_month_from_today()
    s.save()
