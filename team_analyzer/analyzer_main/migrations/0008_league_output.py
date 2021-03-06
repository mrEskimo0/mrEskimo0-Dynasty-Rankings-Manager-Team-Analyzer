# Generated by Django 3.2.5 on 2022-02-01 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer_main', '0007_league'),
    ]

    operations = [
        migrations.CreateModel(
            name='league_output',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.CharField(max_length=30, null=True)),
                ('name', models.CharField(max_length=30, null=True)),
                ('date', models.DateField(blank=True)),
                ('value', models.FloatField(default=0, null=True)),
                ('position', models.CharField(max_length=30, null=True)),
                ('display_name', models.CharField(max_length=30, null=True)),
            ],
            options={
                'db_table': 'league_output',
            },
        ),
    ]
