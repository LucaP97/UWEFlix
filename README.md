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


generic student account:
username: aa
password: LMicyb8=O



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