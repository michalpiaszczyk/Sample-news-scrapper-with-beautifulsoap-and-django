# Generated by Django 4.1.7 on 2023-03-28 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nius', '0005_alter_news_is_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='data',
            field=models.DateField(),
        ),
    ]
