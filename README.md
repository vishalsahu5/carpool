# carpool

## Before Setup
Make sure you have these in your system.

**Python Version-3.5/3.6**

**Django Version-1.11**

## Setup Instructions

1. Make a folder 'project'.
2. Inside that directory, make a Virtual Environment
3. Whenever working with project, make sure you activate the virtualenv.
4. Now inside project folder, git clone the project repo.
5. Activate the virtualenv and cd into carpool.
6. Issue this command in terminal: pip install -r requirements.txt
7. In Project/carpool-master/carpool/settings.py Go to last line and use your own Google API key.
8. In the previous step, get an API Key from google.
9. delete db.sqlite3 from Project/carpool-master/
10. Also delete any migrations directory.

### Commands to be executed

python manage.py makemigrations

python manage.py migrate

python manage.py runserver
