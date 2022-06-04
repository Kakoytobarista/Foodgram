# Проект Foodgram
![example workflow](https://github.com/HeyAslan/foodgram-project-react/actions/main.yml/badge.svg)
### http://foodgram.myvnc.com/recipes

Дипломный проект курса Python-разработчик от Яндекс.Практикум

«Продуктовый помощник» — сайт, на котором можно публиковать рецепты и подписываться на публикации других авторов. Понравившиеся рецепты можно добавить в избранное. Сервис «Список покупок» позволяет скачать список продуктов, которые понадобятся для приготовления выбранных блюд.

После запуска проекта документация доступна по адресу: http://localhost/redoc/

### Технологии:
Python 3.8.5, Django 3.0.5, Django REST framework 3.12.4
PostgreSQL, Docker, Gunicorn, Nginx

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
