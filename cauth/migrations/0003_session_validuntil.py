# Generated by Django 3.2.8 on 2021-10-25 08:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cauth', '0002_account_passw_salt'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='validuntil',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 25, 11, 38, 17, 575891)),
        ),
    ]
