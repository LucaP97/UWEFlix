# UWEFlix

***********************************************************************************
When creating your virtual environment, please use this command:
'py -3 -m venv .venv'
This is required due to the setup of '.gitignore'
To activate the virtual environment: '.venv\scripts\activate'

Once you have created the virtual environment, you will need to run this command:
'pip install -r requirements.txt'
***********************************************************************************

super user credentials
username: admin
password: LMicyb8=O

LOGIN STEPS IN BACKEND:

    1.  enter user details
    2.  copy access key
    3.  got to ModHeader
    4.  press "+" button and "Request header"
    5.  in "Name" enter - Authorization
    6.  in "Value" enter - JTW <access key>
    6.  go back to /uweflix, check top right corner to see "cinema1"
        this means you are logged in


Link to Trello: https://trello.com/b/J8gx00a2/sprints


Link to Jira: https://uweflixgroup3.atlassian.net/jira/software/projects/UW/boards/1/backlog


Club rep:
username: 358673
password: kZZu0YehVJJG


Docker:
- redis:
docker run -d -p 6379:6379 redis


Celery:
celery -A cinema .... loglevel=info
- worker
- beat
- flower


heroku:
https://git.heroku.com/uweflix-prod.git