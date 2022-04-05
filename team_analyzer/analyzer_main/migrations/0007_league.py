# Generated by Django 3.2.5 on 2022-01-27 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('analyzer_main', '0006_auto_20220127_1825'),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, null=True)),
                ('league_id', models.CharField(max_length=30)),
                ('draft_order', models.CharField(choices=[('Max Points For', 'Max Points For'), ('Standings', 'Standings')], default='Max Points For', max_length=264)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_ranking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='analyzer_main.user_ranking')),
            ],
        ),
    ]
