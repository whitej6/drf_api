# Generated by Django 2.2.11 on 2020-03-18 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_restaurant_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]