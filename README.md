# simple-webauth
## INSTALLATION HOW-TO
```
pip3 install -r requirements.txt
python3 manage.py runserver
```
Follow the link shown in runserver command output to view the webpage.

## DOCKER SETUP
1. Install Docker Compose: https://docs.docker.com/compose/install/
2. Create project
```
docker-compose run web django-admin startproject proj
```
3. Create superuser account
```
docker-compose run web python manage.py createsuperuser
```
4. Run server
```
docker-compose up
```
5. Done
___
The default port is 8000
___
