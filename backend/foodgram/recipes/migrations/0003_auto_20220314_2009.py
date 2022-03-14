# Generated by Django 2.2.16 on 2022-03-14 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220308_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favorite',
            field=models.ManyToManyField(related_name='favorites', to='recipes.Recipe', verbose_name='Избранное'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='in_card',
            field=models.ManyToManyField(related_name='card', to='recipes.Recipe', verbose_name='В корзине'),
        ),
    ]
