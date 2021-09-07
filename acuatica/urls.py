# coding=utf-8
from django.conf.urls import url, include
from django.urls import path

from acuatica import views


urlpatterns = [
    url(r'^$', views.index_view, name='acuatica.index'),
    url(r'^login/$', views.login_view, name='acuatica.login'),
    url(r'^register/$', views.register_view, name='acuatica.register'),
    url(r'^logout/$', views.logoutUser, name='acuatica.logout'),
    url(r'^venta-normal/$', views.SalesView.as_view(), name='acuatica.sales.view'),
    url(r'^venta-normal-add/$', views.sales, name='acuatica.sales'),
    url(r'^clientes/$', views.clients, name='acuatica.clientes'),
    url(r'^catalogo/$', views.catalogo, name='acuatica.catalogo'),
    url(r'^entradas/$', views.inputs, name='acuatica.inputs'),
    url(r'^reporte-ventas/$', views.sales_report, name='acuatica.sales-report'),
    url(r'^inv-save/$', views.inv_save, name='acuatica.inv-save'),
    url(r'^sales-charge/$', views.sales_charge, name='acuatica.sales-charge'),
    url(r'^sale-ticket/$', views.ticket, name='acuatica.sales-ticket'),
    url(r'^cancela-venta/(?P<pk>\d+)/$', views.cancel_sale, name='acuatica.cancel-sale'),
]
