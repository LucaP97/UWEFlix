import datetime
import requests
from celery import shared_task


def is_last_day_of_month():
    today = datetime.date.today()
    last_day_of_month = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
    return today == last_day_of_month

@shared_task
def generate_statement():
    if is_last_day_of_month():
        url = 'http://127.0.0.1:8000/accounts/statements/'

        response = requests.post(url)

        if response.status_code == 201:
            print('statement generated')
        else:
            print('statement not generated')