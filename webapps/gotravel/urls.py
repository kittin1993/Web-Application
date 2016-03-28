"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from gotravel import views as private_views

urlpatterns = [
    url(r'^$', private_views.home, name='home'),
    #url(r'^photo/([a-zA-Z0-9]*)/$',private_views.get_photo, name ='get_photo'),
    url(r'^editprofile', private_views.edit_profile, name='editprofile'),
    url(r'^addplan', private_views.add_plan, name='addplan'),
    url(r'^addnote', private_views.add_note, name='addnote'),
    #url(r'^addtitle/(\d+)$', private_views.add_title, name='addtitle'),
    url(r'^searchnote', private_views.search_note, name='searchnote'),
    url(r'^searchplan', private_views.search_plan, name='searchplan'),
    #url(r'^addday/(\d+)$', private_views.add_day, name='addday'),
    #url(r'^adddetail/(\d+)$', private_views.add_detail, name='adddetail'),
    url(r'^myschedule_plan', private_views.myschedule_plan, name='myschedule_plan'),
    url(r'^myschedule_note', private_views.myschedule_note, name='myschedule_note'),
    url(r'^travelnotes', private_views.travelnotes, name='travelnotes'),
    url(r'^travelplans', private_views.travelplans, name='travelplans'),
    url(r'^seenote/(\d+)$', private_views.see_note, name='seenote'),
    url(r'^seeplan/(\d+)$', private_views.see_plan, name='seeplan'),
    url(r'^get_rests_json', private_views.get_rests_json, name='get_rests_json'),
    url(r'^get_hotels_json', private_views.get_hotels_json, name='get_hotels_json'),
    url(r'^login$', auth_views.login, {'template_name':'login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$', private_views.register, name='register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        private_views.confirm_registration, name='confirm'),
]
