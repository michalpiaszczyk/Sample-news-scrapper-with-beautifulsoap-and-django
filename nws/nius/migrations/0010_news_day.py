# Generated by Django 4.1.7 on 2023-03-28 13:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nius', '0009_alter_news_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='day',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]