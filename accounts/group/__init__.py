from django.views.generic import ListView, View, TemplateView
from django.contrib.auth.models import Group, Permission, ContentType
from django.http import JsonResponse, Http404,HttpResponse
from django.db import IntegrityError
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin
from accounts.forms import GroupForm
from django.http import QueryDict
import json


class GroupListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = "auth.view_group"
    permission_redirect_field_name = "index"
    model = Group
    template_name = "user/grouplist.html"


class GroupCreateView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required= "auth.add_group"
    permission_redirect_field_name = "index"
    def post(self, request):
        ret = {"status":0}
        group_name = request.POST.get("name", "")
        if not group_name:
            ret['status'] = 1
            ret['errmsg'] = "用户组不能为空"
            return JsonResponse(ret)
        try:
            g = Group(name=group_name)
            g.save()
        except IntegrityError:
            ret['status'] = 1
            ret['errmsg'] = "用户组已存在"
        """
        g = Group()
        g.name = group_name
        g.save()
        """
        return JsonResponse(ret)


class GroupUserList(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = "user/group_userlist.html"
    permission_required = "auth.view_group"
    permission_redirect_field_name = "index"
    def get_context_data(self, **kwargs):
        context = super(GroupUserList, self).get_context_data(**kwargs)
        # 将指定用户组内的成员列表取出来，然后传给模板
        gid = self.request.GET.get("gid", "")

        try:
            group_obj = Group.objects.get(id=gid)
            context['object_list'] = group_obj.user_set.all()
        except Group.DoesNotExist:
            raise Http404("group does not exist")
        context['gid'] = gid
        return context


class ModifyGroupPermissionList(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    permission_required = "auth.change_group"
    permission_redirect_field_name = "index"

    template_name = "user/modify_group_permissions.html"
    
    def get_context_data(self, **kwargs):
        context = super(ModifyGroupPermissionList, self).get_context_data(**kwargs)
        context["contenttypes"] = ContentType.objects.all()
        context["group"] = self.request.GET.get("gid")
        context["group_permissions"] = self.get_group_permissions(context["group"])
        return context

    def get_group_permissions(self, groupid):
        try:
            group_obj = Group.objects.get(pk=groupid)
            return [p.id for p in group_obj.permissions.all()]
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="用户组不存在")


    def post(self, request):
        permission_id_list = request.POST.getlist("permission", [])
        groupid = request.POST.get("groupid", 0)
        try:
            group_obj = Group.objects.get(pk=groupid)
        except Group.DoesNotExist:
            return redirect("error", next="group_list", msg="用户组不存在")

        if len(permission_id_list) > 0:
            permission_objs = Permission.objects.filter(id__in=permission_id_list)
            group_obj.permissions.set(permission_objs)
        else:
            group_obj.permissions.clear()
        return redirect("success", next="group_list")


# 展示组内拥有的权限
class ShowGroupPermissionList(LoginRequiredMixin,View):
    def get(self,request):
        if not request.user.has_perm('accounts.view_group'):
            return HttpResponse("Forbidden")
        else:
            group_name = request.GET.get("name","")
            print(group_name)
            if group_name:
                try:
                    group_object= Group.objects.get(name=group_name)
                    permissions= group_object.permissions.all()
                except Exception as e:
                    print(e)
                    ret={"status":1,"errmsg":e.args}
                    return JsonResponse(ret)
                permission_list=[]
                for permission in permissions:
                    app = permission.content_type.app_label
                    model = permission.content_type.model
                    codename =permission.codename
                    name = permission.name
                    permission_dict = {"app":app,"model":model,"codename":codename,"name":name}
                    permission_list.append(permission_dict)
                ret={"status":0,"permission_list":permission_list}
            else:
                ret={"status":1,"errmsg":"请输入组名"}
            return JsonResponse(ret)


# 删除组
# 有用户的不能删，有权限的不能删
class GroupDeleteView(LoginRequiredMixin,View):

    def delete(self,request):
        if not request.user.has_perm('accounts.delete_group'):
            return HttpResponse("Forbidden")
        else:
            res={"status":0}
            query_data = QueryDict(request.body)
            group_form = GroupForm(query_data)
            if group_form.is_valid():
                try:
                    Group.objects.get(name__exact=group_form.cleaned_data.get("name")).delete()
                except Exception as e:
                    res["status"]=1
                    res["errmsg"]=e.args[0]
                    return  JsonResponse(res)
                res["status"]=0
            else:
                res["status"]=1
                res["errmsg"]=json.dumps(json.loads(group_form.errors.as_json()),ensure_ascii=False)
                #print(json.dumps(json.loads(group_form.errors_as_json()),ensure_ascii=False))
                #return redirect("error",next="group_list",msg=json.dumps(json.loads(group_form.errors_as_json()),ensure_ascii=False))
            return  JsonResponse(res)
            #return redirect("success",next="group_list")



