# GroupChat-Django
Groupchat is a simple Django web app using Django channels and Rest framework 

## Features
- Admin can add or modify users
- Authentication using Simple JWT
- Users can create Groups and add, remove users in the group
- Send/receive messages in group
- Like messages and view likes 

## Installation

- 1 - Clone repo https://github.com/Sathwik57/GroupChat-Django.git
- 2 - Cd into project
- 3 - Change environment variables
- 4 - Using Docker 
- * - Run the local.yml using docker-compose -f local.yml up --build 
- 5-  Create a virtual environment and activate(Without Docker)  
- * - pip install -r requirements.txt
- * - Migrate using command python manage.py makemigrations and migrate
- * - python manage.py runserver
