# Project Foodgram

![Workflow](https://github.com/KakoytoBarista/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
<br>

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
* Docker/Docker-compose
* Gunicorn
* Nginx
* HTML/CSS/JS
* React
* Redax

## Local Project Launch:
___
Clone the repository and navigate to the infra/ directory:
  
```  
> git clone https://github.com/yankovskaya-ktr/foodgram-project-react.git
> cd foodgram-project-react/infra
``` 

Create a .env file based on the .env.template:

```
> cd infra
> chmod +x ./create_env_file.sh
> ./create_env_file.sh

```
Launch the application:

``` 
> docker-compose up -d --build
``` 
___
### Credentials:

Regular user:

```username: john```

```email: john@gmail.com```

```password: johntest```

Admin user:

```username: admin```

```email: admin@gmail.com```

```password: admintest```
___
### Resources:

#### Main page:
```
> http://localhost/
```
Documentation API:
```
> http://localhost/api/docs/
```
