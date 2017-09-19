from django.shortcuts import render
from django.views.generic import ListView
from issue.models import IssueRecord
# Create your views here.


class ListIssueRecordView(ListView):
    model = IssueRecord
    template_name = "list_issue_record.html"
