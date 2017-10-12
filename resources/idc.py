from django.views.generic import TemplateView, ListView,View
from django.shortcuts import redirect, reverse
from django.http import HttpResponse,JsonResponse,QueryDict
from resources.models import Idc
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin
from .forms import CreateIdcForm,DeleteIdcForm
from dashboard.common import get_errors_message

# 创建idc
class CreateIdcView(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    permission_required = "resources.add_idc"
    permission_redirect_field_name = "index"
    template_name = "idc/add_idc.html"
    def post(self, request):
        form_data = CreateIdcForm(request.POST)
        #print(form_data.is_valid())
        if form_data.is_valid():
            data = form_data.cleaned_data
            print(data)
            try:
                idc=Idc(**data)
                idc.save()
            except  Exception as e:
                return redirect("error", next="idc_add", msg=e.args)
        else:
            return redirect("error", next="idc_add", msg="验证错误")
        return redirect("success", next="idc_list")



# 展示idc信息
class IdcListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = "resources.view_idc"
    permission_redirect_field_name = "index"
    model = Idc
    template_name = "idc/idc_list.html"


# 删除idc
class DeleteIdcView(View):
    def delete(self,request):
        res={"status":0}
        form_data = DeleteIdcForm(QueryDict(request.body))
        if form_data.is_valid():
            try:
                Idc.objects.get(id__exact=form_data.cleaned_data["id"]).delete()
            except Exception as e:
                print(e)
                res["status"] = 1
                res["errmsg"] = "删除发生异常"
        else:
            errmsg = form_data.errors.as_data()
            #print(get_errors_message(errmsg))
            res["status"] = 1
            res["errmsg"] =get_errors_message(errmsg)
        return JsonResponse(res)






