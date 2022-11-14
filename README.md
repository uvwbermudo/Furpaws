============ SET UP ===================

Initial Requirements:
- Python 3.9 
- pipenv 

---- After Cloning the Repository ----
start by creating pipenv environment and install dependencies from the pipfile

Configure your git username and email for idenfication purposes:
https://support.atlassian.com/bitbucket-cloud/docs/configure-your-dvcs-username-for-commits/

BEFORE ADDING ANY NEW FILE:
Make sure you are in the correct branch.

File structure should look like this:

|/flaskr
|---/sample-project                 (your project/page/feature)
|------- __init__.py
|------- forms.py
|------- controller.py
|--- /templates                      (will contain HTML templates)
|------- /sample-project-templates   (will contain templates used in sample-project folder)
|--- /static          
|--- models.py
|--- __init__.py
| config.py
| run.py
| .flaskenv
| .env
| .gitignore
| .Pipfile
| .Pipfile.lock


.env should contain all the variables that you can see in config.py
.flaskenv should contain:
    *sample*
FLASK_APP=run.py
FLASK_ENV=development
FLASK_RUN_PORT=8080