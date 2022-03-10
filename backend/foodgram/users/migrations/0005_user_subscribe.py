# Generated by Django 2.2.16 on 2022-03-10 21:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220309_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscribe',
            field=models.ManyToManyField(related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Подписка'),
        ),
    ]
