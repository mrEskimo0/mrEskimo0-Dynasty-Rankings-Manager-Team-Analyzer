# Generated by Django 3.2.5 on 2021-12-06 18:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer_main', '0002_my_league_my_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='ranking',
            name='date_last_updated',
            field=models.DateTimeField(blank=True, default=datetime.date.today),
        ),
    ]
