# Generated by Django 4.1.4 on 2022-12-09 20:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beauty_salon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='client_entries', to=settings.AUTH_USER_MODEL, verbose_name='клиент'),
        ),
    ]
