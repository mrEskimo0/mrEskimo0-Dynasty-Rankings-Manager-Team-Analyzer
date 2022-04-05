# Generated by Django 3.2.5 on 2021-11-30 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer_main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='My_League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('league_id', models.CharField(max_length=30)),
                ('team_name', models.CharField(max_length=50)),
                ('total_value', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='My_Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=50)),
                ('asset', models.CharField(max_length=50)),
                ('asset_id', models.CharField(max_length=25)),
                ('value', models.FloatField(default=1, null=True)),
            ],
        ),
    ]