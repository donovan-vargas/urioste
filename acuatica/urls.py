# coding=utf-8
from django.conf.urls import url, include
from acuatica import views


urlpatterns = [
    url(r'^$', views.index_view, name='acuatica.index'),
    url(r'^login/$', views.login_view, name='acuatica.login'),
    url(r'^logout/$', views.logout_view, name='acuatica.logout'),
]
