from django.conf.urls import include, url
from issue import views

urlpatterns = [
    url(r'issue_record/', include([
        url(r'list/$', views.ListIssueRecordView.as_view(),name="issue_record_list"),
        #url(r'list/$', idc.IdcListView.as_view(), name="idc_list"),
    ]))
]
