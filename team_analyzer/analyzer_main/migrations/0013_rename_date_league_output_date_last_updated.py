# Generated by Django 3.2.5 on 2022-02-08 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyzer_main', '0012_table_league_total_league_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='league_output',
            old_name='date',
            new_name='date_last_updated',
        ),
    ]