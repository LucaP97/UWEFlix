from celery import shared_task
from .models import CinemaManager
from datetime import datetime

@shared_task
def delete_expired_temporary_cinema_managers():
    expired_cinema_managers = CinemaManager.objects.filter(expiration_date__isnull=False, expiration_date__lte=datetime.now().date())
    expired_cinema_managers.delete()