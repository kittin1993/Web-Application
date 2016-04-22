from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from gotravel.choice import *
from datetime import date


# Create your models here.


class Plan(models.Model):
    owner = models.ForeignKey(User)
    plan_title = models.CharField(max_length=200, blank=True, default="Untitled")
    intro = models.CharField(max_length = 256, blank=True)
    total_day = models.IntegerField(blank=True, default=0)
    creation_time = models.DateTimeField()
    likes = models.IntegerField(blank=True, default=0)
    dislikes = models.IntegerField(blank=True, default=0)
    followers = models.IntegerField(blank=True, default=0)

    def __unicode__(self):
        return self

    def __str__(self):
        return self.__unicode__()


class PlanDetail(models.Model):
    plan = models.ForeignKey(Plan, related_name='plandetail')
    time = models.DateField(blank=True, default=date.today, null=True)
    state = models.CharField(max_length = 256, blank=True)
    county = models.CharField(max_length = 256, blank=True)
    place = models.CharField(max_length=256, blank=True)
    address = models.CharField(max_length=256, blank=True)
    content = models.CharField(max_length=256, blank=True)
    creation_time = models.DateTimeField()

    def __unicode__(self):
        return self

    def __str__(self):
        return self.__unicode__()


class Note(models.Model):
    owner = models.ForeignKey(User)
    creation_time = models.DateTimeField()
    note_title = models.CharField(max_length=200, blank=True, default="Untitled")
    title_image = models.CharField(max_length=256, blank=True, default='https://yumengxemr.s3.amazonaws.com/id-None')
    tag = models.CharField(max_length=256, null=True)
    likes = models.IntegerField(blank=True, default=0)
    dislikes = models.IntegerField(blank=True, default=0)
    total_cost = models.IntegerField(blank=True, default=0)
    followers = models.IntegerField(blank=True, default=0)

    def __unicode__(self):
        return self

    def __str__(self):
        return self.__unicode__()


class NoteDetail(models.Model):
    note = models.ForeignKey(Note, related_name='notedetail')
    time = models.DateField(blank=True, default=date.today, null=True)
    place = models.CharField(max_length=256, blank=True)
    content = models.CharField(max_length=512, blank=True)
    # picture = models.CharField(max_length = 256, blank = True)
    cost = models.CharField(max_length=20, blank=True)
    creation_time = models.DateTimeField()

    def __unicode__(self):
        return self

    def __str__(self):
        return self.__unicode__()


class Noteimage(models.Model):
    notedetail = models.ForeignKey(NoteDetail, related_name='noteimage')
    picture = models.CharField(max_length=256, blank=True)
    creation_time = models.DateTimeField()

    def __unicode__(self):
        return self

    def __str__(self):
        return self.__unicode__()


class Profile(models.Model):
    owner = models.OneToOneField(User)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    age = models.CharField(blank=True, max_length=20)
    gender = models.CharField(blank=True, max_length=10, choices=GENDER_CHOICES, default='M')
    bio = models.CharField(blank=True, max_length=430)
    image_url = models.CharField(max_length=256, blank=True, default='https://yumengxemr.s3.amazonaws.com/id-2')
    P_favorite = models.ManyToManyField(Plan, blank=True, related_name="p_f")
    N_favorite = models.ManyToManyField(Note, blank=True, related_name="n_f")

    # followers = models.ManyToManyField("self", blank = True)

    def __unicode__(self):
        return self

    def __str__(self):
        return self.__unicode__()
