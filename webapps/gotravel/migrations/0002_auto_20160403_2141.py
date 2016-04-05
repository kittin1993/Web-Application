# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-03 21:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gotravel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noteimage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.CharField(blank=True, max_length=256)),
                ('creation_time', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='notedetail',
            name='picture',
        ),
        migrations.AddField(
            model_name='noteimage',
            name='notedetail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noteimage', to='gotravel.NoteDetail'),
        ),
    ]