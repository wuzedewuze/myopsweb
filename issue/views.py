from django.shortcuts import render
from django.views.generic import ListView,View
from issue.models import IssueRecord
from django.http import JsonResponse
# Create your views here.
import datetime
from issue import forms
from issue import  models

class ListIssueRecordView(ListView):
    model = IssueRecord
    template_name = "list_issue_record.html"
    ordering = "-id"

    paginate_by = 15
    before_range_num = 5
    after_range_num = 4

    def get_queryset(self):
        queryset = super(ListIssueRecordView, self).get_queryset()
        search_project = self.request.GET.get("search_project", None)
        start_date = self.request.GET.get("start_date",None )
        end_date = self.request.GET.get("end_date", None)
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        print(today_date)
        if search_project:
            queryset = queryset.filter(project_name__icontains=search_project)
        if start_date:
            queryset = queryset.filter(issue_time__gt=datetime.datetime.strptime(start_date,'%Y-%m-%d'))
        else:
            queryset = queryset.filter(issue_time__gt=today_date)
        if end_date:
            queryset = queryset.filter(issue_time__lt=datetime.datetime.strptime(end_date,'%Y-%m-%d'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListIssueRecordView, self).get_context_data(**kwargs)
        context['page_range'] = self.get_pagerange(context['page_obj'])
        # 处理搜索条件
        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        context['search_data'] = "&" + search_data.urlencode()
        return context

    # 分页设置
    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num
        if start <= 0:
            start = 1
        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end + 1)

    # 新增发布操作
    def post(self,request):
        res = {"status":0}
        issue_date = forms.CreateIssueForm(request.POST)
        if issue_date.is_valid():
            try:
                issue_time = datetime.datetime.now()
                data = models.IssueRecord(**issue_date.cleaned_data)
                data.issue_time = issue_time
                data.save()
            except:
                res["status"]=1
                res["errmsg"]="保存发布内容出现异常"
        else:
            res["status"]=1
            res["errmsg"]="验证不通过"
        return JsonResponse(res)


