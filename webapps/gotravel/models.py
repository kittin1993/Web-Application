from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from gotravel.choice import *
'''
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
'''
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
    plan_title = models.CharField(max_length = 200)
    creation_time = models.DateTimeField()
    likes = models.IntegerField(blank = True, default = 0)
    dislikes = models.IntegerField(blank = True, default = 0)

    def __unicode__(self):
        return self
    def __str__(self):
        return self.__unicode__()

class PlanDetail(models.Model):
    plan = models.ForeignKey(Plan,related_name='plandetail')
    time = models.DateField()
    place = models.CharField(max_length = 256)
    #state = models.CharField(max_length = 256)
    #county = models.CharField(max_length = 256)
    intro = models.CharField(max_length = 256, blank = True)
    creation_time = models.DateTimeField()

    def __unicode__(self):
        return self
    def __str__(self):
        return self.__unicode__()

class Note(models.Model):
    owner = models.ForeignKey(User)
    creation_time = models.DateTimeField()
    note_title = models.CharField(max_length = 200, blank = True)
    title_image = models.CharField(max_length = 256, blank = True, default='https://yumengxemr.s3.amazonaws.com/id-None')
    likes = models.IntegerField(blank = True, default = 0)
    dislikes = models.IntegerField(blank = True, default = 0)
    total_cost = models.IntegerField(blank = True, default = 0)

    def __unicode__(self):
        return self
    def __str__(self):
        return self.__unicode__()

class NoteDetail(models.Model):
    note = models.ForeignKey(Note,related_name='notedetail')
    time = models.DateField()
    place = models.CharField(max_length = 256, blank = True)
    content = models.CharField(max_length = 512, blank = True)
    #picture = models.CharField(max_length = 256, blank = True)
    cost = models.CharField(max_length = 20, blank = True)
    creation_time = models.DateTimeField()
    
    def __unicode__(self):
        return self
    def __str__(self):
        return self.__unicode__() 

class Noteimage(models.Model):
    notedetail = models.ForeignKey(NoteDetail,related_name='noteimage')
    picture = models.CharField(max_length = 256, blank = True)
    creation_time = models.DateTimeField()
    
    def __unicode__(self):
        return self
    def __str__(self):
        return self.__unicode__() 




