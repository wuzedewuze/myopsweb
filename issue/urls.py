from django.conf.urls import include, url
from issue import views

urlpatterns = [
    url(r'issue_record/', include([
        url(r'list/$', views.ListIssueRecordView.as_view(),name="issue_record_list"),
        url(r'add/$', views.AddIssueView.as_view(), name="issue_record_add"),
        url(r'delete/$', views.DeleteIssueView.as_view(), name="issue_record_delete"),
        url(r'change/$',views.ChangeIssueStatusView.as_view(), name="issue_record_change"),
        url(r'test/$',views.big_file_download,name="test_export"),
    ]))
]
