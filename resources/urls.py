from django.conf.urls import include, url

from . import idc
from resources import server

urlpatterns = [
    url(r'idc/', include([
        url(r'add/$', idc.CreateIdcView.as_view(), name="idc_add"),
        url(r'list/$', idc.IdcListView.as_view(), name="idc_list"),
        url(r'delete/$',idc.DeleteIdcView.as_view(),name="idc_delete")
    ])),
    url(r'server/',include([
        url(r'report/$',server.ServerInfoAuto,name="server_report")
    ]))
]
