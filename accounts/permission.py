from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import Permission, ContentType
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.mixins import PermissionRequiredMixin


class PermissionListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    permission_required = "auth.view_permission"
    permission_redirect_field_name = "index"
    model = Permission
    template_name = "user/permission_list.html"
    paginate_by = 10
    ordering = "id"

    def get_queryset(self):
        queryset = super(PermissionListView,self).get_queryset()
        search_model = self.request.GET.get("search_model")
        search_codename = self.request.GET.get("search_codename")

        if search_codename:
            queryset = queryset.filter(codename__icontains=search_codename)
        if search_model:
            queryset = queryset.filter(content_type_id__model__contains=search_model)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PermissionListView,self).get_context_data(**kwargs)
        #search_model = self.request.GET.get("search_model")
        #search_codename = self.request.GET.get("search_codename")
        search_data=self.request.GET.copy()
        print(search_data)
        context.update(search_data.dict())
        return context



class PermissionCreateView(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = "user/add_permission.html"
    permission_required = "auth.add_permission"
    permission_redirect_field_name = "index"
    def get_context_data(self, **kwargs):
        context = super(PermissionCreateView, self).get_context_data(**kwargs)
        context['contenttypes'] = ContentType.objects.all()
        return context
    def post(self, request):
        content_type_id = request.POST.get("content_type")
        codename = request.POST.get("codename")
        name = request.POST.get("name")
        try:
            content_type = ContentType.objects.get(pk=content_type_id)
        except ContentType.DoesNotExist:
            return redirect("error", next="permission_list", msg="模型不存在")
        if not codename or codename.find(" ") >=0 :
            return redirect("error", next="permission_list", msg="codename 不合法")
        try:
            Permission.objects.create(codename=codename, content_type=content_type,name=name)
        except Exception as e:
            return redirect("error", next="permission_list", msg=e.args)
        return redirect("success", next="permission_list")


