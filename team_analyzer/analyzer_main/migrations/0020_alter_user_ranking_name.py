# Generated by Django 3.2.5 on 2022-04-11 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer_main', '0019_user_ranking_duplicate ranking name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_ranking',
            name='name',
            field=models.CharField(max_length=75),
        ),
    ]
