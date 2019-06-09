from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.showusers, name='index'),
    url(r'^(?P<user>\d+)/$', views.CreateRoom.as_view()),
    url(r'^chat/(?P<chatid>[^/]+)/$', views.ShowRoom.as_view(), name='room'),
]