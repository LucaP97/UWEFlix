from celery.schedules import schedule
from datetime import timedelta
from django.utils import timezone
import calendar

class LastDayOfMonthSchedule(schedule):
    def is_due(self, last_run_at):
        now = self.now()
        days_in_current_month = calendar.monthrange(now.year, now.month)[1]

        if now.day == days_in_current_month and (now - last_run_at) > timedelta(days=1):
            remaining = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_in_current_month) - now
            return True, remaining
        else:
            return False, timedelta(days=1)
