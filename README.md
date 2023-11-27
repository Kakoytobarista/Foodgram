# Project Foodgram

![Workflow](https://github.com/yankovskaya-ktr/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

<br>
Link on host: http://aslangram.ddns.net/recipes

___


The backend and partially the frontend are developed by me. Backend development, partial frontend development, containerization, deploying the project on a virtual machine, CI/CD, configuring daemons, setting up Nginx, and configuring the Gunicorn server for Django, as well as Docker Compose configuration.

It is the final project of the Python Developer course from Yandex.Praktikum.

"Product Assistant" is a website where users can publish recipes and subscribe to publications from other authors. Favorite recipes can be added to the favorites list. The "Shopping List" service allows users to download a list of products needed for selected dishes.

After launching the project, documentation is available at: http://localhost/redoc/

Technologies:
* Python 3.8.5
* Django 3.0.5
* Django REST framework 3.12.4
* PostgreSQL
* Docker
* Gunicorn
* Nginx

## Local Project Launch:
### Clone the repository and navigate to the infra/ directory:
  
```  
> git clone https://github.com/yankovskaya-ktr/foodgram-project-react.git
> cd foodgram-project-react/infra
``` 

Create a .env file based on the .env.template:

```
> cp .env.template .env
```
Launch the application:

``` 
> docker-compose up
``` 
Perform migrations:

``` 
> docker-compose exec web python manage.py migrate --noinput
``` 

Create a superuser:


``` 
> docker-compose exec web python manage.py createsuperuser
``` 

Import data into the database:
  
```  
> docker-compose exec web python manage.py import_data
```

### Resources:

Main page:
```
http://localhost/
```
Documentation API:
```
http://localhost/api/docs/redoc.html
```
