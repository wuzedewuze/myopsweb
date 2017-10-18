from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.http import JsonResponse, QueryDict
from django.views.generic import ListView, View

from accounts.mixins import PermissionRequiredMixin
from accounts.models import Profile
from accounts.user.forms import AddUserForm
from dashboard.common import get_errors_message
import  logging
logger = logging.getLogger("myself")
# 查看用来列表
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "auth.view_user"
    permission_redirect_field_name = "index"
    template_name = "user/userlist.html"
    model = User
    paginate_by = 8
    before_range_num = 4
    after_range_num = 4
    ordering = "id"

    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        queryset = queryset.filter(is_superuser=False)
        username = self.request.GET.get("search_username", None)
        logger.debug(queryset)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)

        # 当前页  的前7条
        context['page_range'] = self.get_pagerange(context['page_obj'])
        # 处理搜索条件
        context['search_username']="" # 设置默认为空
        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except:
            pass
        context.update(search_data.dict())
        context['search_data'] = "&" + search_data.urlencode()
        return context

    def get_pagerange(self, page_obj):
        current_index = page_obj.number
        start = current_index - self.before_range_num
        end = current_index + self.after_range_num
        if start <= 0:
            start = 1
        if end >= page_obj.paginator.num_pages:
            end = page_obj.paginator.num_pages
        return range(start, end + 1)

    # @method_decorator(permission_required("auth.add_user", login_url=reverse("error",kwargs={"next":"dashboard", "msg":"没有权限，请联系管理员"})))
    # @method_decorator(permission_required("auth.add_user",login_url="/"))
    def get(self, request, *args, **kwargs):
        return super(UserListView, self).get(request, *args, **kwargs)


# 修改用户状态
class ModifyUserStatusView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "auth.change_user"
    permission_redirect_field_name = "index"

    def post(self, request):
        uid = request.POST.get("uid", "")
        ret = {"status": 0}
        try:
            user_obj = User.objects.get(id=uid)
            # user_obj.is_active = False if user_obj.is_active else True
            if user_obj.is_active:
                user_obj.is_active = False
            else:
                user_obj.is_active = True
            user_obj.save()
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"

        return JsonResponse(ret)


# 修改用户组
class ModifyUserGroupView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ("auth.change_user", "auth.delete_user")
    permission_redirect_field_name = "index"

    def get(self, request):
        print(request.GET)
        uid = request.GET.get('uid', "")
        group_objs = Group.objects.all()
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
        else:
            group_objs = group_objs.exclude(id__in=user_obj.groups.values_list("id"))
        return JsonResponse(list(group_objs.values("id", "name")), safe=False)

    def put(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)
        uid = data.get("uid", "")
        gid = data.get("gid", "")
        try:
            user_obj = User.objects.get(id=uid)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
            return JsonResponse(ret)
        try:
            group_obj = Group.objects.get(id=gid)
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
            return JsonResponse(ret)
        user_obj.groups.add(group_obj)
        return JsonResponse(ret)

    def delete(self, request):
        ret = {"status": 0}
        data = QueryDict(request.body)
        try:
            user_obj = User.objects.get(id=data.get('uid', ""))
            group_obj = Group.objects.get(id=data.get('gid', ""))
            user_obj.groups.remove(group_obj)

            # group_obj.user_set.remove(user_obj)
        except User.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户不存在"
        except Group.DoesNotExist:
            ret['status'] = 1
            ret['errmsg'] = "用户组不存在"
        return JsonResponse(ret)


# 新增用户类
class AddUserView(View):
    def post(self, request):
        res = {"status": 0}
        user_data = AddUserForm(request.POST)
        if user_data.is_valid():
            try:
                user = {"username": user_data.cleaned_data["username"], "email": user_data.cleaned_data["email"],}
                user_obj = User(**user)
                user_obj.set_password(user_data.cleaned_data["password"])
                user_obj.save()
                profile = {"user": user_obj, "name": user_data.cleaned_data["name"],
                           "phone": user_data.cleaned_data["phone"], "weixin": user_data.cleaned_data["weixin"]}
                Profile(**profile).save()
            except Exception as e:
                print(e)
                res["status"] = 1
                res["errmsg"] = "保存发布发生异常，请查看后台日志"
        else:
            err = user_data.errors.as_data()
            res["status"] = 1
            res["errmsg"] = get_errors_message(err)
        return JsonResponse(res)
