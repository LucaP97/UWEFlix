# UWEFlix
**********************************************************************************
in models.py:

ticket type and price are now back to choices fields
    
showing has been changed from "OneToOneField" to "ForeignKey" as OneToOne does not allow for multiple tickets to have the same showing object whilst ForeignKey         does as it is a "one to many" type of relationship

in views.py:

No child tickets will be made if booking for an 18 movie - an error message will show if an attempt is made

**********************************************************************************
test booking inputs:

{
    "film": "spiderman",
    "screen": "1",
    "showing_time": "2023-03-29 12:00:00+00:00",
    "student": 0,
    "adult": 0,
    "child": 0
}

{
    "film": "Batman",
    "screen": "2",
    "showing_time": "2023-03-10 12:34:56+00:00",
    "student": 0,
    "adult": 0,
    "child": 0
}


**********************************************************************************

added booking logic - can now input amount of tickts wanted

need to adjust it so that it creates amount of tickts corresponding to the amount of Adult tickets, Child tickets and Student tickets


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


Link to Jira: https://uweflixgroup3.atlassian.net/jira/software/projects/UW/boards/1/backlog
