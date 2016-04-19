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
    # url(r'^photo/([a-zA-Z0-9]*)/$',private_views.get_photo, name ='get_photo'),
    url(r'^editprofile', private_views.edit_profile, name='editprofile'),
    url(r'^addplan', private_views.add_plan, name='addplan'),
    url(r'^addnote', private_views.add_note, name='addnote'),
    url(r'^map', private_views.map, name='map'),
    # url(r'^addtitle/(\d+)$', private_views.add_title, name='addtitle'),
    url(r'^invite/(\d+)$', private_views.invite, name='invite'),
    url(r'^searchnote', private_views.search_note, name='searchnote'),
    url(r'^searchplan', private_views.search_plan, name='searchplan'),
    # url(r'^addday/(\d+)$', private_views.add_day, name='addday'),
    # url(r'^adddetail/(\d+)$', private_views.add_detail, name='adddetail'),
    url(r'^myschedule_plan', private_views.myschedule_plan, name='myschedule_plan'),
    url(r'^myschedule_note', private_views.myschedule_note, name='myschedule_note'),
    url(r'^myschedule_favorite', private_views.myschedule_favorite, name='myschedule_favorite'),
    url(r'^travelnotes', private_views.travelnotes, name='travelnotes'),
    url(r'^travelplans', private_views.travelplans, name='travelplans'),
    url(r'^seenote/(\d+)$', private_views.see_note, name='seenote'),
    url(r'^addlikes/(\d+)$', private_views.add_likes, name='addlikes'),
    url(r'^adddislikes/(\d+)$', private_views.add_dislikes, name='adddislikes'),
    url(r'^addfavorite/(\d+)$', private_views.add_favorite, name='addfavorite'),
    url(r'^addplikes/(\d+)$', private_views.add_plikes, name='addplikes'),
    url(r'^addpdislikes/(\d+)$', private_views.add_pdislikes, name='addpdislikes'),
    url(r'^addpfavorite/(\d+)$', private_views.add_pfavorite, name='addpfavorite'),
    url(r'^deletenote/(\d+)$', private_views.delete_note, name='deletenote'),
    url(r'^editnote/(\d+)$', private_views.edit_note, name='editnote'),
    url(r'^editplan/(\d+)$', private_views.edit_plan, name='editplan'),
    url(r'^seeplan/(\d+)$', private_views.see_plan, name='seeplan'),
    url(r'^deleteplan/(\d+)$', private_views.delete_plan, name='deleteplan'),
    #url(r'^get_rests_json', private_views.get_rests_json, name='get_rests_json'),
    #url(r'^get_hotels_json', private_views.get_hotels_json, name='get_hotels_json'),
    url(r'^password_reset$', auth_views.password_reset, {'template_name': 'password_reset.html'},
        name='password_reset'),
    url(r'^password_reset_done$', auth_views.password_reset_done, {'template_name': 'password_reset_done.html'},
        name='password_reset_done'),
    # url(r'^forgotpass', private_views.forgot_pass, name='forgotpass'),
    url(r'^resetconfirm/(?P<uidb64>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        auth_views.password_reset_confirm, {'template_name': 'password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^password_reset_complete$', auth_views.password_reset_complete,
        {'template_name': 'password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^login$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$', private_views.register, name='register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        private_views.confirm_registration, name='confirm'),
    url(r'^search_destination', private_views.search_destination, name='search_destination'),
]
