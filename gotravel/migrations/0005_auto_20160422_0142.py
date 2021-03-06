# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 01:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gotravel', '0004_note_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='plandetail',
            name='address',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='plandetail',
            name='county',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='plandetail',
            name='place',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='plandetail',
            name='state',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
