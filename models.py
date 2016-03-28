from django.db import models
from django.contrib.auth.models import User
import os


class Profile(models.Model):
	owner = models.OneToOneField(User)
	last_name = models.CharField(max_length = 30)
	first_name = models.CharField(max_length = 30)
	age = models.CharField(blank = True, max_length = 20)
	gender = models.CharField(blank = True, max_length = 20)
	bio = models.CharField(blank = True, max_length = 430)
	image = models.CharField(max_length = 256, blank = True, default='https://yumengxemr.s3.amazonaws.com/id-2')
	followers = models.ManyToManyField("self", blank = True)

	def __unicode__(self):
		return self
	def __str__(self):
		return self.__unicode__()

class Schedule(models.Model):
	owner = models.ForeignKey(User)
	plantitle = models.CharField(max_length = 20)

	def __unicode__(self):
		return self
	def __str__(self):
		return self.__unicode__()

class NewPlan(models.Model):
	owner = models.ForeignKey(User)
	planid = models.CharField(max_length = 256)
	time = models.DateTimeField()
	place = models.CharField(max_length = 256)
	intro = models.CharField(max_length = 256, blank = True)

	def __unicode__(self):
		return self
	def __str__(self):
		return self.__unicode__()

class OldPlan(models.Model):
	owner = models.ForeignKey(User)
	time = models.DateTimeField()
	place = models.CharField(max_length = 256, blank = True)
	note = models.CharField(max_length = 512, blank = True)
	picture = models.CharField(max_length = 256, blank = True)
	video = models.CharField(max_length = 256, blank = True)
	cost = models.CharField(max_length = 20, blank = True)
	time = models.DateTimeField(auto_now = True)
	
	def __unicode__(self):
		return self
	def __str__(self):
		return self.__unicode__() 



