# Generated by Django 4.1.7 on 2023-03-28 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nius', '0008_alter_news_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='data',
            field=models.DateTimeField(),
        ),
    ]
