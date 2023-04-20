import requests
from celery import shared_task

@shared_task
def generate_statement():
    url = 'http://127.0.0.1:8000/accounts/statements/'
    # headers = {'Content-Type', 'application/json'}

    response = requests.post(url)#, headers=headers)

    if response.status_code == 201:
        print('statement generated')
    else:
        print('statement not generated')