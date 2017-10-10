from django.conf.urls import include, url
from issue import views

urlpatterns = [
    url(r'issue_record/', include([
        url(r'list/$', views.ListIssueRecordView.as_view(),name="issue_record_list"),
        url(r'add/$', views.AddIssueView.as_view(), name="issue_record_add"),
        url(r'delete/$', views.DeleteIssueView.as_view(), name="issue_record_delete"),
        url(r'change/$',views.ChangeIssueStatusView.as_view(), name="issue_record_change"),
        url(r'download/$',views.DownLoadExcelView.as_view(),name="download_excel"),
        url(r'change_issue',views.ChangeIssueView.as_view(),name="issue_change")
    ]))
]
