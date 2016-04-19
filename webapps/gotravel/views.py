from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.core import serializers
from django.db.models import Q
import json, random
from datetime import datetime
from datetime import date
import datetime as dt
from django.contrib.auth.views import password_reset, password_reset_confirm

import urllib2
import demjson


# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from django.forms import formset_factory
from gotravel.models import *
from gotravel.forms import *
from gotravel.s3 import *
from gotravel.test_yelp import *


# Create your views here.
# @login_required
def home(request):
    username = request.user.username
    if not username:
        print username
        notes = Note.objects.all()
        plans = Plan.objects.all()
        context = {'username': "Visitor", 'notes': notes, 'plans': plans}
        return render(request, 'homepage.html', context)

    new_user = User.objects.get(username=username)
    notes = Note.objects.all().order_by('-likes')[:6]
    plans = Plan.objects.all().order_by('-likes')[:12]
    # print posts
    context = {'username': username, 'new_user': new_user, 'notes': notes, 'plans': plans}
    return render(request, 'homepage.html', context)


@login_required
def add_plan(request):
    context = {}
    username = request.user
    context['username'] = username
    new_user = User.objects.get(username=username)

    if request.method == 'GET':
        form = EditPlanForm()
        context['form'] = form
        return render(request, 'addplan.html', context)

    creation_time = datetime.now()
    plan = Plan(owner=new_user, creation_time=creation_time)
    form = EditPlanForm(request.POST, instance=plan)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'addplan.html', context)

    form.save()

    print request.POST
    print request.POST.getlist('place')
    length = len(request.POST.getlist('place'))
    print length
    plan = Plan.objects.get(owner=new_user, creation_time=creation_time)
    for index in range(length):
        print index
        plandetail = PlanDetail(plan=plan, creation_time=datetime.now())
        plandetail.place = request.POST.getlist('place')[index]
        plandetail.time = request.POST.getlist('time')[index]
        plandetail.intro = request.POST.getlist('des')[index]
        plandetail.save()

    plandetails = PlanDetail.objects.filter(plan=plan)
    context['new_user'] = new_user
    context['plan'] = plan
    context['plandetails'] = plandetails
    return redirect(reverse('seeplan', args=(plan.id,)))


# return render(request, 'seeplan.html', context)
@login_required
def get_rests_json(request):
    restaurants = get_restaurant('pittsburgh')

    # hotels = get_hotel('pittsburgh')
    res_dic = []
    # hot_dic = {}
    for res in restaurants:
        new_res = {}
        new_res['url'] = res.url
        new_res['name'] = res.name
        new_res['image_url'] = res.image_url
        new_res['location'] = res.location.address
        new_res['phone'] = res.phone
        # print new_res
        res_dic.append(new_res)

    response_json = json.dumps(res_dic)

    return HttpResponse(response_json, content_type='application/json')


@login_required
def get_hotels_json(request):
    hotels = get_hotel('pittsburgh')

    hotel_dic = []
    for hotel in hotels:
        new_hotel = {}
        new_hotel['url'] = hotel.url
        new_hotel['name'] = hotel.name
        new_hotel['image_url'] = hotel.image_url
        new_hotel['location'] = hotel.location.address
        new_hotel['phone'] = hotel.phone
        hotel_dic.append(new_hotel)

    response_json = json.dumps(hotel_dic)

    return HttpResponse(response_json, content_type='application/json')


"""
@login_required
def add_day(request, noteid):
	note = Note.objects.get(id=noteid)
	print dt.date.today()
	notedetail = NoteDetail(note=note,time=dt.date.today())
	noted_dic = {}
	noted_dic['id'] = notedetail.id
	noted_dic['place'] = notedetail.place
	noted_dic['time'] = notedetail.time.strftime("%b. %d, %Y")
	noted_dic['cost'] = notedetail.cost
	noted_dic['content'] = notedetail.content
	response_json=json.dumps(noted_dic)

	return HttpResponse(response_json, content_type='application/json')

@login_required
def add_detail(request, noteid):
	context={}
	print request
	return render(request, 'addnote.html', context)
"""


@login_required
def add_note(request):
    context = {}
    username = request.user
    context['username'] = username
    new_user = User.objects.get(username=username)
    # note = Note(owner=new_user, creation_time=datetime.now())
    # note.save()

    if request.method == 'GET':
        form = EditNoteForm()
        context['form'] = form
        return render(request, 'addnote.html', context)

    # print request.FILES['title_image']
    creation_time = datetime.now()
    note = Note(owner=new_user, creation_time=creation_time)
    form = EditNoteForm(request.POST, request.FILES, instance=note)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'addnote.html', context)

    if form.cleaned_data['title_image']:
        print "have image"
        url = s3_upload(form.cleaned_data['title_image'], random.random())
        note.title_image = url

    form.save()

    print request.POST
    print request.POST.getlist('place')
    print request.FILES.getlist('picture0')
    length = len(request.POST.getlist('place'))
    print length
    note = Note.objects.get(owner=new_user, creation_time=creation_time)
    for index in range(length):
        print index
        notedetail = NoteDetail(note=note, creation_time=datetime.now())
        notedetail.place = request.POST.getlist('place')[index]
        notedetail.time = request.POST.getlist('time')[index]
        notedetail.content = request.POST.getlist('content')[index]
        notedetail.cost = request.POST.getlist('cost')[index]
        notedetail.save()
        pic_name = "picture" + str(index)
        print request.FILES.getlist(pic_name)
        for num in range(len(request.FILES.getlist(pic_name))):
            noteimage = Noteimage(notedetail=notedetail, creation_time=datetime.now())
            image_url = s3_upload(request.FILES.getlist(pic_name)[num], random.random())
            noteimage.picture = image_url
            noteimage.save()

    notedetails = NoteDetail.objects.filter(note=note)
    context['new_user'] = new_user
    context['note'] = note
    context['notedetails'] = notedetails

    return redirect(reverse('seenote', args=(note.id,)))


# return render(request, 'addnote.html', context)
"""
@login_required
def add_title(request, noteid):
	context={}
	note = Note.objects.get(id=noteid)
	note.note_title=request['notetitle']
	print request
	return render(request, 'addnote.html', context)
@login_required
def add_note(request):
	context = {}
	username = request.user
	context['username']= username
	new_user = User.objects.get(username=username)
	creation_time = datetime.now()
	note = Note(owner=new_user,note_title="Edit Title Here",creation_time=creation_time)
	note.save()
	context['note'] = note
	return render(request,'addnote.html', context)
"""


@login_required
def map(request):
    username = request.user
    new_user = User.objects.get(username=username)
    user_profile = Profile.objects.get(owner=new_user)

    context = {'username': username, 'new_user': new_user, 'user_profile': user_profile}
    return render(request, 'googleboundary.html', context)


@login_required
def see_note(request, id):
    try:
        username = request.user
        new_user = User.objects.get(username=username)
        user_profile = Profile.objects.get(owner=new_user)
        note = Note.objects.get(id=id)

        if NoteDetail.objects.filter(note=note).exists():
            alldetail = NoteDetail.objects.filter(note=note)
            context = {'username': username, 'new_user': new_user, 'user_profile': user_profile, 'note': note,
                       'alldetail': alldetail}
            return render(request, 'seenote.html', context)

        context = {'username': username, 'new_user': new_user, 'user_profile': user_profile, 'note': note}
        return render(request, 'seenote.html', context)
    except Note.DoesNotExist:
        new_user = User.objects.get(username=request.user)
        notes = Note.objects.all()
        context = {'message': 'Note with id={0} does not exist'.format(id), 'notes': notes, 'new_user': new_user}
        return render(request, 'travelnotes.html', context)


@login_required
def add_likes(request, id):
    note = Note.objects.get(id=id)
    note.likes = note.likes + 1
    note.save()
    context = {}
    context['likes'] = note.likes
    response_json = json.dumps(context)

    return HttpResponse(response_json, content_type='application/json')


@login_required
def add_dislikes(request, id):
    note = Note.objects.get(id=id)
    note.dislikes = note.dislikes + 1
    note.save()
    context = {}
    context['dislikes'] = note.dislikes
    response_json = json.dumps(context)

    return HttpResponse(response_json, content_type='application/json')


@login_required
def add_favorite(request, id):
    context = {}
    note = get_object_or_404(Note, id=id)
    user = get_object_or_404(User, username=request.user)
    print "return note"
    # note.followers.add(user)
    if not Note.objects.filter(id=id, n_f=user.profile).exists():
        note.followers = note.followers + 1
        note.save()
        user.profile.N_favorite.add(note)

    num = note.followers
    print num
    context['num'] = num
    response_json = json.dumps(context)

    return HttpResponse(response_json, content_type='application/json')


@login_required
def add_pfavorite(request, id):
    context = {}
    plan = get_object_or_404(Plan, id=id)
    user = get_object_or_404(User, username=request.user)
    print "return note"
    # note.followers.add(user)
    if not Plan.objects.filter(id=id, p_f=user.profile).exists():
        plan.followers = plan.followers + 1
        plan.save()
        user.profile.P_favorite.add(plan)

    num = plan.followers
    print num
    context['num'] = num
    response_json = json.dumps(context)

    return HttpResponse(response_json, content_type='application/json')


@login_required
def add_plikes(request, id):
    plan = Plan.objects.get(id=id)
    plan.likes = plan.likes + 1
    plan.save()
    context = {}
    context['likes'] = plan.likes
    response_json = json.dumps(context)

    return HttpResponse(response_json, content_type='application/json')


@login_required
def add_pdislikes(request, id):
    plan = Plan.objects.get(id=id)
    plan.dislikes = plan.dislikes + 1
    plan.save()
    context = {}
    context['dislikes'] = plan.dislikes
    response_json = json.dumps(context)

    return HttpResponse(response_json, content_type='application/json')


@login_required
def delete_note(request, id):
    username = request.user
    new_user = User.objects.get(username=username)
    user_profile = Profile.objects.get(owner=new_user)
    note = Note.objects.get(id=id)

    if NoteDetail.objects.filter(note=note).exists():
        alldetail = NoteDetail.objects.filter(note=note)
        for detail in alldetail:
            if Noteimage.objects.filter(notedetail=detail).exists():
                allimage = Noteimage.objects.filter(notedetail=detail)
                for image in allimage:
                    image.delete()
            detail.delete()
    note.delete()

    notes = Note.objects.filter(owner=new_user)
    # print posts
    context = {'username': username, 'new_user': new_user, 'notes': notes}
    return render(request, 'myschedule_note.html', context)


@login_required
def edit_note(request, id):
    try:
        alldetails = []
        if request.method == 'GET':
            print "get"
            note = Note.objects.get(id=id)
            noteform = EditNoteForm(instance=note)
            detailforms = []
            # DetailFormSet = formset_factory(EditNoteDetailForm)

            num = 0
            if NoteDetail.objects.filter(note=note).exists():
                alldetail = NoteDetail.objects.filter(note=note)
                for detail in alldetail:
                    detail_set = {}
                    detail_set['detail'] = detail
                    detail_set['time'] = datetime.strptime(str(detail.time), "%Y-%m-%d")
                    print detail_set['time']
                    detail_set['num'] = num
                    alldetails.append(detail_set)
                    num = num + 1
                    # for detail in alldetail:
                    #	print "test"
                    #	detailform = EditNoteDetailForm(instance=detail)
                    #	detailforms.append(detailform)
                    #	print detailform

            context = {'note': note, 'noteform': noteform, 'alldetails': alldetails, 'detailforms': detailforms}
            return render(request, 'edit_note.html', context)

        # entry = Entry.objects.select_for_update().get(id=id)
        # db_update_time = entry.update_time  # Copy timestamp to check after form is bound
        print request.POST.getlist('place')
        note = Note.objects.get(id=id)
        detailforms = []
        noteform = EditNoteForm(request.POST, request.FILES, instance=note)
        if not noteform.is_valid():
            num = 0
            if NoteDetail.objects.filter(note=note).exists():
                alldetail = NoteDetail.objects.filter(note=note)
                for detail in alldetail:
                    detail_set = {}
                    detail_set['detail'] = detail
                    detail_set['time'] = datetime.strptime(detail.time, "%Y-%m-%d")
                    print detail_set['time']
                    detail_set['num'] = num
                    alldetails.append(detail_set)
                    num = num + 1
            context = {'note': note, 'noteform': noteform, 'alldetails': alldetails}
            return render(request, 'edit_note.html', context)

        noteform.save()

        if NoteDetail.objects.filter(note=note).exists():
            alldetail = NoteDetail.objects.filter(note=note)
            for detail in alldetail:
                if Noteimage.objects.filter(notedetail=detail).exists():
                    allimage = Noteimage.objects.filter(notedetail=detail)
                    for image in allimage:
                        image.delete()
                detail.delete()

        print request.POST
        print request.POST.getlist('place')
        print request.FILES.getlist('picture0')
        length = len(request.POST.getlist('place'))
        print length
        for index in range(length):
            print index
            notedetail = NoteDetail(note=note, creation_time=datetime.now())
            notedetail.place = request.POST.getlist('place')[index]
            if not request.POST.getlist('time')[index]:
                notedetail.time = datetime.now()
            else:
                notedetail.time = request.POST.getlist('time')[index]
            notedetail.content = request.POST.getlist('content')[index]
            notedetail.cost = request.POST.getlist('cost')[index]
            notedetail.save()
            pic_name = "picture" + str(index)
            print request.FILES.getlist(pic_name)
            for number in range(len(request.FILES.getlist(pic_name))):
                noteimage = Noteimage(notedetail=notedetail, creation_time=datetime.now())
                image_url = s3_upload(request.FILES.getlist(pic_name)[number], random.random())
                noteimage.picture = image_url
                noteimage.save()

        # form = EditForm(instance=entry)
        context = {
            'message': 'note updated.',
            'note': note,
            'noteform': noteform,
        }
        return redirect(reverse('seenote', args=(note.id,)))
    except Note.DoesNotExist:
        new_user = User.objects.get(username=request.user)
        notes = Note.objects.filter(owner=new_user)
        context = {'message': 'Note with id={0} does not exist'.format(id), 'notes': notes, 'new_user': new_user}
        return render(request, 'myschedule_note.html', context)


@login_required
def edit_plan(request, id):
    try:
        alldetails = []
        if request.method == 'GET':
            print "get"
            note = Note.objects.get(id=id)
            noteform = EditNoteForm(instance=note)
            detailforms = []
            # DetailFormSet = formset_factory(EditNoteDetailForm)

            num = 0
            if NoteDetail.objects.filter(note=note).exists():
                alldetail = NoteDetail.objects.filter(note=note)
                for detail in alldetail:
                    detail_set = {}
                    detail_set['detail'] = detail
                    detail_set['time'] = datetime.strptime(str(detail.time), "%Y-%m-%d")
                    print detail_set['time']
                    detail_set['num'] = num
                    alldetails.append(detail_set)
                    num = num + 1
                    # for detail in alldetail:
                    #	print "test"
                    #	detailform = EditNoteDetailForm(instance=detail)
                    #	detailforms.append(detailform)
                    #	print detailform

            context = {'note': note, 'noteform': noteform, 'alldetails': alldetails, 'detailforms': detailforms}
            return render(request, 'edit_note.html', context)

        # entry = Entry.objects.select_for_update().get(id=id)
        # db_update_time = entry.update_time  # Copy timestamp to check after form is bound
        print request.POST.getlist('place')
        note = Note.objects.get(id=id)
        detailforms = []
        noteform = EditNoteForm(request.POST, request.FILES, instance=note)
        if not noteform.is_valid():
            num = 0
            if NoteDetail.objects.filter(note=note).exists():
                alldetail = NoteDetail.objects.filter(note=note)
                for detail in alldetail:
                    detail_set = {}
                    detail_set['detail'] = detail
                    detail_set['time'] = datetime.strptime(detail.time, "%Y-%m-%d")
                    print detail_set['time']
                    detail_set['num'] = num
                    alldetails.append(detail_set)
                    num = num + 1
            context = {'note': note, 'noteform': noteform, 'alldetails': alldetails}
            return render(request, 'edit_note.html', context)

        noteform.save()

        if NoteDetail.objects.filter(note=note).exists():
            alldetail = NoteDetail.objects.filter(note=note)
            for detail in alldetail:
                if Noteimage.objects.filter(notedetail=detail).exists():
                    allimage = Noteimage.objects.filter(notedetail=detail)
                    for image in allimage:
                        image.delete()
                detail.delete()

        print request.POST
        print request.POST.getlist('place')
        print request.FILES.getlist('picture0')
        length = len(request.POST.getlist('place'))
        print length
        for index in range(length):
            print index
            notedetail = NoteDetail(note=note, creation_time=datetime.now())
            notedetail.place = request.POST.getlist('place')[index]
            if not request.POST.getlist('time')[index]:
                notedetail.time = datetime.now()
            else:
                notedetail.time = request.POST.getlist('time')[index]
            notedetail.content = request.POST.getlist('content')[index]
            notedetail.cost = request.POST.getlist('cost')[index]
            notedetail.save()
            pic_name = "picture" + str(index)
            print request.FILES.getlist(pic_name)
            for number in range(len(request.FILES.getlist(pic_name))):
                noteimage = Noteimage(notedetail=notedetail, creation_time=datetime.now())
                image_url = s3_upload(request.FILES.getlist(pic_name)[number], random.random())
                noteimage.picture = image_url
                noteimage.save()

        # form = EditForm(instance=entry)
        context = {
            'message': 'note updated.',
            'note': note,
            'noteform': noteform,
        }
        return redirect(reverse('seenote', args=(note.id,)))
    except Plan.DoesNotExist:
        new_user = User.objects.get(username=request.user)
        plans = Plan.objects.filter(owner=new_user)
        context = {'message': 'Note with id={0} does not exist'.format(id), 'plans': plans, 'new_user': new_user}
        return render(request, 'myschedule_plan.html', context)


@login_required
def delete_plan(request, id):
    username = request.user
    new_user = User.objects.get(username=username)
    user_profile = Profile.objects.get(owner=new_user)
    plan = Plan.objects.get(id=id)

    if PlanDetail.objects.filter(plan=plan).exists():
        alldetail = PlanDetail.objects.filter(plan=plan)
        for detail in alldetail:
            detail.delete()
    plan.delete()

    plans = Plan.objects.filter(owner=new_user)
    # print posts
    context = {'username': username, 'new_user': new_user, 'plans': plans}
    return render(request, 'myschedule_plan.html', context)


@login_required
def see_plan(request, id):
    try:
        username = request.user
        new_user = User.objects.get(username=username)
        user_profile = Profile.objects.get(owner=new_user)
        plan = Plan.objects.get(id=id)
        # print posts
        context = {'username': username, 'new_user': new_user, 'user_profile': user_profile, 'plan': plan}
        return render(request, 'seeplan.html', context)
    except Plan.DoesNotExist:
        new_user = User.objects.get(username=request.user)
        plans = Plan.objects.all()
        context = {'message': 'Plan with id={0} does not exist'.format(id), 'plans': plans, 'new_user': new_user}
        return render(request, 'travelplans.html', context)


@login_required
def invite(request, id):
    print request.POST
    sender_name = request.POST['name']
    sender_email = request.POST['email']
    sender_message = request.POST['message']
    username = request.user
    new_user = User.objects.get(username=username)
    user_profile = Profile.objects.get(owner=new_user)
    plan = Plan.objects.get(id=id)
    receiver = plan.owner
    receiver_name = receiver.username
    receiver_email = receiver.email

    email_body = sender_message + "\n\nMy name:" + sender_name + "\nMy email:" + sender_email

    subject = "[From GoTravel]Hi," + receiver_name + "! Someone wants to invite you to travel together"
    send_mail(subject=subject,
              message=email_body,
              from_email="yumengx@andrew.cmu.edu",
              recipient_list=[receiver_email])
    # print posts
    context = {'username': username, 'new_user': new_user, 'user_profile': user_profile, 'plan': plan}
    return render(request, 'seeplan.html', context)


@login_required
def myschedule_plan(request):
    username = request.user
    new_user = User.objects.get(username=username)
    plans = Plan.objects.filter(owner=new_user)
    # print posts
    context = {'username': username, 'new_user': new_user, 'plans': plans}
    return render(request, 'myschedule_plan.html', context)


@login_required
def myschedule_note(request):
    username = request.user
    new_user = User.objects.get(username=username)
    notes = Note.objects.filter(owner=new_user)
    # print posts
    context = {'username': username, 'new_user': new_user, 'notes': notes}
    return render(request, 'myschedule_note.html', context)


@login_required
def myschedule_favorite(request):
    username = request.user
    new_user = User.objects.get(username=username)
    notes = Note.objects.filter(n_f=new_user.profile)
    plans = Plan.objects.filter(p_f=new_user.profile)
    # print posts
    context = {'username': username, 'new_user': new_user, 'notes': notes, 'plans': plans}
    return render(request, 'myschedule_favorite.html', context)


# @login_required
def travelnotes(request):
    username = request.user.username
    if not username:
        print username
        notes = Note.objects.all().order_by('-creation_time')
        context = {'username': "Visitor", 'notes': notes}
        return render(request, 'travelnotes.html', context)

    new_user = User.objects.get(username=username)
    notes = Note.objects.all().order_by('-creation_time')
    # print posts
    context = {'username': username, 'new_user': new_user, 'notes': notes}
    return render(request, 'travelnotes.html', context)


@login_required
def search_note(request):
    username = request.user.username
    new_user = User.objects.get(username=username)
    print request.POST
    keyword = request.POST['keyword']
    order = request.POST['order']
    result = []

    if order == 2:
        notes = Note.objects.all().order_by("likes")
    elif order == 1:
        notes = Note.objects.all().order_by("total_cost")
    else:
        notes = Note.objects.all().order_by("-creation_time")

    for note in notes:
        if keyword.lower() in note.note_title.lower():
            result.append(note)
        else:
            if note.notedetail.filter(Q(content__icontains=keyword) | Q(place__icontains=keyword)).exists():
                result.append(note)
    # print posts
    context = {'username': username, 'new_user': new_user, 'result': result}
    return render(request, 'notesresult.html', context)


@login_required
def search_plan(request):
    username = request.user.username
    new_user = User.objects.get(username=username)
    place = request.POST['place']
    time = request.POST['time']
    result = []
    plans = Plan.objects.all()
    for plan in plans:
        if plan.plandetail.filter(place=place, time=time).exists():
            result.append(plan)
    # print posts
    context = {'username': username, 'new_user': new_user, 'result': result}
    return render(request, 'plansresult.html', context)


# @login_required
def travelplans(request):
    username = request.user.username
    if not username:
        print username
        plans = Plan.objects.all().order_by('-creation_time')
        context = {'username': "Visitor", 'plans': plans}
        return render(request, 'travelplans.html', context)

    new_user = User.objects.get(username=username)
    plans = Plan.objects.all().order_by('-creation_time')
    context = {'username': username, 'new_user': new_user, 'plans': plans}
    return render(request, 'travelplans.html', context)


@login_required
def seenotes(request):
    username = request.user
    new_user = User.objects.get(username=username)
    user_profile = Profile.objects.get(owner=new_user)
    # print posts
    context = {'username': username, 'new_user': new_user, 'user_profile': user_profile}
    return render(request, 'travelplans.html', context)


@login_required
def edit_profile(request):
    context = {}
    username = request.user
    context['username'] = username

    user_profile = get_object_or_404(Profile, owner=User.objects.get(username=username))
    new_user = User.objects.get(username=username)

    if request.method == 'GET':
        form = EditProfileForm(instance=user_profile)
        context = {'user_profile': user_profile, 'form': form, 'new_user': new_user}
        return render(request, 'editprofile.html', context)

    form = EditProfileForm(request.POST, request.FILES, instance=user_profile)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'editprofile.html', context)

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


def forgot_pass(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'forgotpass.html', context)

    user = request.POST['username']
    if User.objects.filter(username=user).exists():
        # send email

        new_user = User.objects.get(username=user)
        receiver_email = new_user.email
        receiver_name = new_user.username
        token = default_token_generator.make_token(new_user)
        email_body = """
		You have asked for resetting your password. Please click the link below to verify your email address and
		complete the password resetting of your account:
		http://%s%s
		""" % (request.get_host(), reverse('resetconfirm', args=[new_user.username, token]))
        subject = "[From GoTravel]Hi," + receiver_name + "! This is password resetting email! "
        send_mail(subject=subject,
                  message=email_body,
                  from_email="yumengx@andrew.cmu.edu",
                  recipient_list=[receiver_email])

        context['email'] = receiver_email
        return render(request, 'success.html', context)
    else:
        if User.objects.filter(email=user).exists():
            new_user = User.objects.get(email=user)
            receiver_email = new_user.email
            receiver_name = new_user.username
            token = default_token_generator.make_token(new_user)
            email_body = """
		
			You have asked for resetting your password. Please click the link below to verify your email address and
			complete the password resetting of your account:
			http://%s%s
			""" % (request.get_host(), reverse('resetconfirm', args=[new_user.username, token]))
            subject = "[From GoTravel]Hi," + receiver_name + "! This is password resetting email! "
            send_mail(subject=subject,
                      message=email_body,
                      from_email="yumengx@andrew.cmu.edu",
                      ecipient_list=[receiver_email])

            context['email'] = receiver_email
            return render(request, 'success.html', context)
        else:
            error_msg = "Username or email doesn't exists."
            context = {'error_msg': error_msg}
            return render(request, 'forgotpass.html', context)


def reset_confirm(request, username, token):
    username = username
    token = token
    # Wrap the built-in reset confirmation view and pass to it all the captured parameters like uidb64, token
    # and template name, url to redirect after password reset is confirmed.
    return password_reset_confirm(request, template_name='reset_confirm.html',
                                  username=username, token=token, post_reset_redirect=reverse('success'))


# This view renders a page with success message.
def success(request):
    return render(request, "success.html")


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

    # create_form = EditProfileForm(instance=profile)

    # Validates the form.
    if not form.is_valid():
        return render(request, 'registration.html', context)

    # If we get here the form data was valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        last_name=form.cleaned_data['last_name'],
                                        first_name=form.cleaned_data['first_name'],
                                        email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
    new_user.is_active = False
    new_user.save()
    # new_user = form.save()

    print 'username' + new_user.username
    profile = Profile(owner=User.objects.get(username=form.cleaned_data['username']),
                      last_name=form.cleaned_data['last_name'], first_name=form.cleaned_data['first_name'])
    profile.is_active = False
    profile.save()

    token = default_token_generator.make_token(new_user)
    email_body = """
	Welcome to go traveling. Please click the link below to verify your email address and
	complete the registration of your account:
	http://%s%s
	""" % (request.get_host(), reverse('confirm', args=[new_user.username, token]))

    send_mail(subject="Verify your email address",
              message=email_body,
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


def search_destination(request):
    destination = request.GET["destination"]
    county = request.GET["county"]
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+destination+"+in+"+county+"&key=AIzaSyC5DNDex1ZhKPKyZZn2zdrkdGo4aZKgx0Q"
    data = urllib2.urlopen(url)
    result_content = data.read()
    print(result_content)
    # places_json = demjson.encode(result_content)
    # print places_json
    # return HttpResponse(places_json, content_type='application/json')
    return HttpResponse(result_content, content_type='application/json')
