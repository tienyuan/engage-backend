# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-07 08:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ingest', '0007_auto_20180303_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('sent', models.PositiveIntegerField(default=0)),
                ('agenda_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='ingest.AgendaItem')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]