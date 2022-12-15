# Проект Foodgram
![example workflow](https://github.com/HeyAslan/foodgram-project-react/actions/workflows/main.yml/badge.svg)
### http://aslangram.ddns.net/recipes

«Продуктовый помощник» — сайт, на котором можно публиковать рецепты и подписываться на 
публикации других авторов. Понравившиеся рецепты можно добавить в 
избранное. Сервис «Список покупок» позволяет скачать список продуктов, которые 
понадобятся для приготовления выбранных блюд.


### Технологии:
Python 3.8.5, Django 3.0.5, Django REST framework 3.12.4
PostgreSQL, Docker, Gunicorn, Nginx.

## Схема моделей, views, serializers в Miro:

```
https://miro.com/app/board/uXjVOJwNSYQ=/
```

### Локальный запуск проекта:

Клонировать репозиторий и перейти в директорию infra/:  
  
```  
> git clone https://github.com/HeyAslan/foodgram-project-react
> cd foodgram-project-react/infra
``` 

Создать файл .env по шаблону .env.template:

```
> cp .env.template .env
```
Запустить приложение:

``` 
> docker-compose up
``` 
Провести миграции:

``` 
> docker-compose exec web python manage.py migrate --noinput
``` 

Создать суперпользователя:

``` 
> docker-compose exec web python manage.py createsuperuser
``` 

Импортировать данные в базу данных:  
  
```  
> docker-compose exec web python manage.py import_data
```

### Ресурсы:

Главная страница:
```
http://localhost/
```
Документация API:
```
http://localhost/api/docs/redoc.html
```# praktikum_new_diplom
