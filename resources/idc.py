from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse
from django.http import HttpResponse
from resources.models import Idc
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin
from .forms import CreateIdcForm


class CreateIdcView(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    permission_required = "resources.add_idc"
    permission_redirect_field_name = "index"
    template_name = "idc/add_idc.html"
    def post(self, request):
        '''
        name = request.POST.get("name", "")
        idc_name = request.POST.get("idc_name", "")
        address = request.POST.get("address", "")
        username = request.POST.get("username", "")
        phone = request.POST.get("user_phone", "")
        email = request.POST.get("mail", "")
        # 2 对数据进行验证
        errmsg = []
        if not name:
            errmsg.append("idc简称不能为空")
        if not idc_name:
            errmsg.append("idc名称不能为空")

        if errmsg:
            return redirect("error", next="idc_add", msg=json.dumps(errmsg))

        # 3 将数据插入到数据库：创建模型对象
        idc = Idc()
        idc.name = name
        idc.idc_name = idc_name
        idc.address = address
        idc.username = username
        idc.phone = phone
        idc.email = email
        try:
            idc.save()
        except Exception as e :
            return redirect("error", next="idc_add", msg=e.args)
        return redirect("success", next="idc_list")
        '''
        form_data = CreateIdcForm(request.POST)
        print(form_data.is_valid())
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



class IdcListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    permission_required = "resources.view_idc"
    permission_redirect_field_name = "index"
    model = Idc
    template_name = "idc/idc_list.html"
