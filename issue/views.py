# coding:utf-8
from django.shortcuts import render
from django.views.generic import ListView, View
from issue.models import IssueRecord
from django.http import JsonResponse,QueryDict,HttpResponse
# Create your views here.
import datetime
from issue import forms
from issue import models

from xlwt import *
import  os
from io import StringIO


class ListIssueRecordView(ListView):
    model = IssueRecord
    template_name = "list_issue_record.html"
    ordering = "-id"

    paginate_by = 10
    before_range_num = 5
    after_range_num = 4

    def get_queryset(self):
        queryset = super(ListIssueRecordView, self).get_queryset()
        search_project = self.request.GET.get("search_project", None)
        start_date = self.request.GET.get("start_date", None)
        end_date = self.request.GET.get("end_date", None)
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        #print(today_date)
        if search_project:
            queryset = queryset.filter(project_name__icontains=search_project)
        if start_date:
            queryset = queryset.filter(issue_time__gt=datetime.datetime.strptime(start_date, '%Y-%m-%d'))
        else:
            queryset = queryset.filter(issue_time__gt=today_date)
        if end_date:
            queryset = queryset.filter(issue_time__lt=datetime.datetime.strptime(end_date, '%Y-%m-%d'))
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



        # 新增发布


    # 下载excel
    def post(self,request):
        date =  self.get_queryset()
        print(date)
        return HttpResponse("ok")










# 新增发布操作
class AddIssueView(View):
    def post(self, request):
        res = {"status": 0}
        issue_date = forms.CreateIssueForm(request.POST)
        if issue_date.is_valid():
            try:
                issue_time = datetime.datetime.now()
                data = models.IssueRecord(**issue_date.cleaned_data)
                data.issue_time = issue_time
                data.save()
            except:
                res["status"] = 1
                res["errmsg"] = "保存发布内容出现异常"
        else:
            res["status"] = 1
            res["errmsg"] = "验证不通过"
        return JsonResponse(res)


# 删除操作
class DeleteIssueView(View):
    def delete(self, request):
        res={"status":0}
        issue_dict = QueryDict(request.body)
        form_date = forms.DeleteIssueForm(issue_dict)
        if form_date.is_valid():
            id = form_date.cleaned_data["id"]
            try:
                models.IssueRecord.objects.get(id=id).delete()
            except Exception as e:
                res["status"] = 1
                res["errmsg"] = "删除发生异常"
        else:
            errmsg = form_date.errors.as_data()
            nice =errmsg["id"]
            #print(nice)
            res["status"] = 1
            res["errmsg"] = ''.join(nice[0])
        return JsonResponse(res)


# 修改发布状态
class ChangeIssueStatusView(View):
    def put(self,request):
        res = {"status":0}
        issue_dict = QueryDict(request.body)
        form_date = forms.ChangeIssueForm(issue_dict)
        if form_date.is_valid():
            try:
                issue_obj = models.IssueRecord.objects.get(id=form_date.cleaned_data["id"])
                print(issue_obj.issue_status)
                if issue_obj.issue_status == "0":
                    issue_obj.issue_status = "1"
                elif issue_obj.issue_status == "1":
                    issue_obj.issue_status = "2"
                elif issue_obj.issue_status == "2":
                    issue_obj.issue_status = "1"
                print(issue_obj.issue_status)
                issue_obj.save()

            except Exception as e:
                print(e)
                res["status"] = 1
                res["errmsg"] = "发生异常"

        else:
            errmsg = form_date.errors.as_data()
            nice =errmsg["id"]
            res["status"] = 1
            res["errmsg"] = ''.join(nice[0])
        return JsonResponse(res)


#

#
def excel_export(request):
    """
    导出excel表格
    """
    # 创建工作薄
    ws = Workbook(encoding='utf-8')
    w = ws.add_sheet(u"发布记录")
    w.write(0, 0, "id")
    w.write(0, 1, u"用户名")
    w.write(0, 2, u"发布时间")
    w.write(0, 3, u"内容")
    w.write(0, 4, u"来源")
    # 保存到本地
    ###########################
    exist_file = os.path.exists("test.xls")
    if exist_file:
        os.remove(r"test.xls")
    ws.save("test.xls")
    ############################

    return HttpResponse("ok")


from django.http import StreamingHttpResponse

def big_file_download(request):
    # do something...

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size).decode('utf-8', 'ignore')
                if c:
                    yield c
                else:
                    break

    the_file_name = "test.txt"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response
