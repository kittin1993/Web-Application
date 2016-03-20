from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from gotravel.choice import *

# Create your models here.
class Profile(models.Model):
	owner = models.OneToOneField(User)
	last_name = models.CharField(max_length = 30)
	first_name = models.CharField(max_length = 30)
	age = models.CharField(blank = True, max_length = 20)
	gender = models.CharField(blank = True, max_length = 10, choices = GENDER_CHOICES, default = 'M')
	bio = models.CharField(blank = True, max_length = 430)
	image_url = models.CharField(max_length = 256, blank = True, default='https://yumengxemr.s3.amazonaws.com/id-2')
	#followers = models.ManyToManyField("self", blank = True)

	def __unicode__(self):
		return self
	def __str__(self):
		return self.__unicode__()

class Plan(models.Model):
	owner = models.ForeignKey(User)
	plan_title = models.CharField(max_length = 20)
	creation_time = models.DateTimeField()

	def __unicode__(self):
		return self
	def __str__(self):
		return self.__unicode__()

class PlanDetail(models.Model):
	plan = models.ForeignKey(Plan)
	time = models.DateField()
	state = models.CharField(max_length = 256)
	county = models.CharField(max_length = 256)
	intro = models.CharField(max_length = 256, blank = True)

	def __unicode__(self):
		return self
	def __str__(self):
		return self.__unicode__()

class Note(models.Model):
	owner = models.ForeignKey(User)
	note_title = models.CharField(max_length = 20, blank = True)
	creation_time = models.DateTimeField()
	title_image = models.CharField(max_length = 256, blank = True, default='https://yumengxemr.s3.amazonaws.com/id-None')

	def __unicode__(self):
		return self
	def __str__(self):
		return self.__unicode__()

class NoteDetail(models.Model):
	note = models.ForeignKey(Note)
	time = models.DateTimeField()
	place = models.CharField(max_length = 256, blank = True)
	content = models.CharField(max_length = 512, blank = True)
	picture = models.CharField(max_length = 256, blank = True)
	video = models.CharField(max_length = 256, blank = True)
	cost = models.CharField(max_length = 20, blank = True)
	
	def __unicode__(self):
		return self
	def __str__(self):
		return self.__unicode__() 
