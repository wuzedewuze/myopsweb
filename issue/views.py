# coding:utf-8
from django.shortcuts import render
from django.views.generic import ListView, View
from issue.models import IssueRecord
from django.http import JsonResponse,QueryDict,HttpResponse
from django.views.generic.list import  MultipleObjectMixin
from accounts.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime
from issue import forms
from issue import models

from xlwt import *
import  os,json
from io import StringIO,BytesIO


class ListIssueRecordView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = "issue.view_issue"
    permission_redirect_field_name = "index"

    model = IssueRecord
    template_name = "list_issue_record.html"
    ordering = "issue_time"

    paginate_by = 10
    before_range_num = 5
    after_range_num = 4

    def get_queryset(self):
        queryset = super(ListIssueRecordView, self).get_queryset()
        search_project = self.request.GET.get("search_project", None)
        search_issue_content = self.request.GET.get("search_issue_content", None)
        start_date = self.request.GET.get("start_date", None)
        end_date = self.request.GET.get("end_date", None)
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        #print(today_date)
        if search_project:
            queryset = queryset.filter(project_name__icontains=search_project)
        if search_issue_content:
            queryset = queryset.filter(issue_content__icontains=search_issue_content)
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





# excel下载类
class DownLoadExcelView(LoginRequiredMixin,PermissionRequiredMixin,MultipleObjectMixin,View):
    permission_required = "issue.export_issue"
    permission_redirect_field_name = "index"

    model = IssueRecord

    def get(self,request,*args, **kwargs):
        # 获取用户信息
        queryset = super(DownLoadExcelView, self).get_queryset()
        search_project = self.request.GET.get("search_project", None)
        start_date = self.request.GET.get("start_date", None)
        end_date = self.request.GET.get("end_date", None)
        today_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if search_project:
            queryset = queryset.filter(project_name__icontains=search_project)
        if start_date:
            queryset = queryset.filter(issue_time__gt=datetime.datetime.strptime(start_date, '%Y-%m-%d'))
        else:
            queryset = queryset.filter(issue_time__gt=today_date)
        if end_date:
            queryset = queryset.filter(issue_time__lt=datetime.datetime.strptime(end_date, '%Y-%m-%d'))
        # 调用生成excel
        # 生成excel文件名
        excel_name = "report-{}".format(today_date)
        #print(queryset)
        res = self.get_excel(queryset,excel_name)
        # 导出excel提供页面下载
        str = BytesIO()
        res.save(str)
        str.seek(0)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename={}.xls'.format(excel_name)
        response.write(str.getvalue())
        return response

    # 生成excel的内部方法保存excel到本地并返回Workbook对象：
    def get_excel(self,object_list,excel_name):
        # 设置头部样式
        style_heading = easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """
                                )
        style_body = easyxf("""
        font:
            name Arial,
            bold off,
            height 0XA0;
        align:
            wrap on,
            vert center,
            horiz left;
        borders:
            left THIN,
            right THIN,
            top THIN,
            bottom THIN;
        """
        )


        style_green = easyxf(" pattern: pattern solid,fore-colour 0x11;")
        style_red = easyxf(" pattern: pattern solid,fore-colour 0x0A;")
        fmts = [
            'M/D/YY',
            'D-MMM-YY',
            'D-MMM',
            'MMM-YY',
            'h:mm AM/PM',
            'h:mm:ss AM/PM',
            'h:mm',
            'h:mm:ss',
            'M/D/YY h:mm',
            'mm:ss',
            '[h]:mm:ss',
            'mm:ss.0',
        ]

        # 创建工作薄
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet(u"发布记录")
        # 写入标题
        w.write(0, 0, u"发布时间",style_heading)
        w.write(0, 1, u"工程名",style_heading)
        w.write(0, 2, u"发布内容",style_heading)
        w.write(0, 3, u"开发人员",style_heading)
        w.write(0, 4, u'测试人员',style_heading)
        w.write(0, 5, u'发布人员',style_heading)
        w.write(0, 6, u'发布状态',style_heading)
        w.write(0, 7, u'svn路径',style_heading)
        w.write(0, 8, u'备注信息',style_heading)

        # 宽度调整
        w.col(0).width = 80*50
        w.col(1).width = 80*50
        w.col(2).width = 300*50
        w.col(3).width = 100*50
        w.col(4).width = 100*50
        w.col(5).width = 50*50
        w.col(6).width = 30*50
        w.col(7).width = 500*50
        w.col(7).width = 300*50

        # 写入内容
        row = 1
        for object in object_list:
            w.write(row,0,object.issue_time.strftime('%Y-%m-%d %H:%M:%S'),style_body)
            w.write(row,1,object.project_name,style_body)
            w.write(row,2,object.issue_content,style_body)
            w.write(row,3,object.dev_person,style_body)
            w.write(row,4,object.test_person,style_body)
            w.write(row,5,object.issue_person,style_body)
            status = "未知状态"
            if object.issue_status == "0":
                status = "未发布"
                w.write(row,6,status,style_red)
            elif object.issue_status == "1":
                status = "已发布"
                w.write(row,6,status,style_green)
            elif object.issue_status == "2":
                status = "已回滚"
                w.write(row,6,status,style_body)

            w.write(row,7,object.svn_path,style_body)
            w.write(row,8,object.remark,style_body)
            row+=1
        # 保存到本地
        ###########################
        #os.mkdir("mytemp")
        excel_file = "{}.xls".format(excel_name)
        exist_file = os.path.exists(excel_file)
        if exist_file:
            os.remove(excel_file)
        ws.save(excel_file)
        ############################
        return ws


# 新增发布操作
class AddIssueView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = "issue.add_issuerecord"
    permission_redirect_field_name = "index"


    def post(self, request):
        res = {"status": 0}
        issue_date = forms.CreateIssueForm(request.POST)
        if issue_date.is_valid():
            try:
                issue_time = datetime.datetime.now()
                data = models.IssueRecord(**issue_date.cleaned_data)
                data.issue_time = issue_time
                data.save()
            except Exception as e:
                print(e)
                res["status"] = 1
                res["errmsg"] = "保存发布发生异常，请查看后台日志"
        else:
            #errmsg = issue_date.errors.as_data()
            #print(errmsg)
            errmsg=json.dumps(json.loads(issue_date.errors.as_json()), ensure_ascii=False)
            #''.join(errmsg["id"][0])
            res["status"] = 1
            res["errmsg"] = errmsg
        return JsonResponse(res)


# 修改发布操作
class ChangeIssueView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = "issue.change_issuerecord"
    permission_redirect_field_name = "index"


    def post(self, request):
        res = {"status": 0}
        issue_date = forms.ChangeIssueForm(request.POST)
        if issue_date.is_valid():
            try:
                id = issue_date.cleaned_data["id"]
                data, create= models.IssueRecord.objects.update_or_create(id=id,defaults=issue_date.cleaned_data,)
            except Exception as e:
                print(e)
                res["status"] = 1
                res["errmsg"] = "保存发布发生异常，请查看后台日志"
        else:
            errmsg=json.dumps(json.loads(issue_date.errors.as_json()), ensure_ascii=False)
            res["status"] = 1
            res["errmsg"] = errmsg
        return JsonResponse(res)


# 删除操作
class DeleteIssueView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = "issue.delete_issuerecord"
    permission_redirect_field_name = "index"


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
class ChangeIssueStatusView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = "issue.change_issuerecord"
    permission_redirect_field_name = "index"

    def put(self,request):
        res = {"status":0}
        issue_dict = QueryDict(request.body)
        form_date = forms.ChangeIssueStatuForm(issue_dict)
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



