from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.core import serializers
import json,random
from datetime import datetime


# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from gotravel.models import *
from gotravel.forms import *
from gotravel.s3 import *

# Create your views here.
@login_required
def home(request):
    print request.user
    username = request.user
    new_user= User.objects.get(username=username)
    notes = Note.objects.all()
    plans = Plan.objects.all()
    #print posts
    context={'username':username,'new_user':new_user, 'notes':notes, 'plans':plans}
    return render(request,'homepage.html',context)

@login_required
def profile(request, author):
    user = get_object_or_404(User, username=author)
    new_user = get_object_or_404(User, username=request.user)
    errors=[]
    print author
    try:
        #pf_user = request.user
        #print pf_user
        print author
        pf_username = User.objects.get(username=author)
        print pf_username
        pf_info = User.objects.get(username=author).get_full_name()
        print "fullname:"+pf_info
        posts = Post.objects.filter(author=User.objects.get(username=author)).order_by('-time')
        print  User.objects.all()
        context = {'pf_username':pf_username,'pf_info':pf_info,'posts':posts,'errors':errors,'new_user':new_user}
    except ValueError as e:
        errors.append(e.message)
        context = {'errors':errors}
    return render(request, 'profile.html', context)

@login_required
def add_plan(request):
    context = {}
    username = request.user
    context['username']= username
    new_user = User.objects.get(username=username)

    if request.method == 'GET':
        form = EditPlanForm()
        context['form']=form
        return render(request,'addplan.html', context)
    
    plan = Plan(owner=new_user, creation_time=datetime.now())
    form = EditPlanForm(request.POST, instance=plan)
    context['form']= form 
    
    if not form.is_valid():
        return render(request,'addplan.html',context)
    
    form.save()
    context['new_user'] = new_user
    context['plan'] = plan
    return render(request, 'addplan.html', context)

@login_required
def add_note(request):
    context = {}
    username = request.user
    context['username']= username
    new_user = User.objects.get(username=username)

    if request.method == 'GET':
        form = EditNoteForm()
        print "edit note form"
        context['form']=form
        return render(request,'addnote.html', context)
    
    note = Note(owner=new_user, creation_time=datetime.now())
    print note.creation_time
    form = EditNoteForm(request.POST, request.FILES, instance=note)
    context['form']= form 
    
    if not form.is_valid():
        return render(request,'addnote.html',context)

    if form.cleaned_data['title_image']:
        print "note id"
        image = s3_upload(form.cleaned_data['title_image'],random.random())
        note.title_image = image
    
    form.save()
    context['new_user'] = new_user
    context['note'] = note
    return render(request, 'addnote.html', context)


@login_required
def see_note(request, id):
    username = request.user
    new_user= User.objects.get(username=username)
    user_profile = Profile.objects.get(owner=new_user)
    note = Note.objects.get(id=id)
    #print posts
    context={'username':username,'new_user':new_user,'user_profile':user_profile,'note':note}
    return render(request,'seenote.html',context)

@login_required
def see_plan(request, id):
    username = request.user
    new_user= User.objects.get(username=username)
    user_profile = Profile.objects.get(owner=new_user)
    plan = Plan.objects.get(id=id)
    #print posts
    context={'username':username,'new_user':new_user, 'user_profile':user_profile,'plan':plan}
    return render(request,'seeplan.html',context)

@login_required
def myschedule_plan(request):
    username = request.user
    new_user= User.objects.get(username=username)
    plans = Plan.objects.filter(owner=new_user)
    #print posts
    context={'username':username,'new_user':new_user, 'plans':plans}
    return render(request,'myschedule_plan.html',context)

@login_required
def myschedule_note(request):
    username = request.user
    new_user= User.objects.get(username=username)
    notes = Note.objects.filter(owner=new_user)
    #print posts
    context={'username':username,'new_user':new_user, 'notes':notes}
    return render(request,'myschedule_note.html',context)

@login_required
def travelnotes(request):
    username = request.user
    new_user= User.objects.get(username=username)
    notes = Note.objects.all()
    #print posts
    context={'username':username,'new_user':new_user, 'notes':notes}
    return render(request,'travelnotes.html',context)

@login_required
def travelplans(request):
    username = request.user
    new_user= User.objects.get(username=username)
    plans = Plan.objects.all()
    context={'username':username,'new_user':new_user, 'plans':plans}
    return render(request,'travelplans.html',context)

@login_required
def seenotes(request):
    username = request.user
    new_user= User.objects.get(username=username)
    user_profile = Profile.objects.get(owner=new_user)
    #print posts
    context={'username':username,'new_user':new_user, 'user_profile':user_profile}
    return render(request,'travelplans.html',context)

@login_required
def edit_profile(request):
    context = {}
    username = request.user
    context['username']= username

    user_profile = get_object_or_404(Profile, owner=User.objects.get(username=username))
    new_user = User.objects.get(username=username)

    if request.method == 'GET':
        form = EditProfileForm(instance=user_profile)
        context = { 'user_profile': user_profile, 'form': form ,'new_user':new_user}
        return render(request, 'editprofile.html', context)

    
    form = EditProfileForm(request.POST, request.FILES, instance= user_profile)
    context['form']= form 
    
    if not form.is_valid():
        return render(request,'editprofile.html',context)

    if form.cleaned_data['image']:
        url = s3_upload(form.cleaned_data['image'], user_profile.id)
        user_profile.image_url = url

    user_profile.gender = form.cleaned_data['gender']
    form.save()
    """
    # update profile information    
    user_profile.age = form.cleaned_data['age']
    user_profile.bio = form.cleaned_data['bio']
    user_profile.save()
    """
    new_user.first_name = form.cleaned_data['first_name']
    new_user.last_name = form.cleaned_data['last_name']
    new_user.save()
    
    context['user_profile'] = user_profile
    context['new_user'] = new_user

    return redirect(reverse('home'))

    
@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'registration.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    #create_form = EditProfileForm(instance=profile)

    # Validates the form.
    if not form.is_valid():
        return render(request, 'registration.html', context)

    # If we get here the form data was valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
        last_name =form.cleaned_data['last_name'],first_name =form.cleaned_data['first_name'],
        email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
    new_user.is_active = False
    new_user.save()
    #new_user = form.save()

    print 'username'+new_user.username
    profile = Profile(owner=User.objects.get(username=form.cleaned_data['username']),
        last_name =form.cleaned_data['last_name'],first_name =form.cleaned_data['first_name'])
    profile.is_active = False
    profile.save()

    token = default_token_generator.make_token(new_user)
    email_body ="""
    Welcome to go traveling. Please click the link below to verify your email address and
    complete the registration of your account:
    http://%s%s
    """ % (request.get_host(),reverse('confirm', args=[new_user.username,token]))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="yumengx@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'confirmation.html', context)

@transaction.atomic
def confirm_registration(request, username, token):
    new_user = get_object_or_404(User, username=username)
    new_profile = get_object_or_404(Profile, owner=new_user)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(new_user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    new_user.is_active = True
    new_user.save()
    new_profile.is_active = True
    new_profile.save()

    return render(request, 'confirmed.html', {})
