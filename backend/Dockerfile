FROM python:3.8.5
WORKDIR /code
COPY requirements.txt .
COPY data/ingredients.json .
RUN pip3 install -r requirements.txt
COPY /foodgram .
CMD [ "sh", "-c", \
"python3 manage.py migrate \
&& \
python3 manage.py collectstatic --noinput && python manage.py loaddata finally_data.json \
&& \
gunicorn foodgram.wsgi:application --bind 0:8000" \
]
