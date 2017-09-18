from django.contrib.auth.mixins import PermissionRequiredMixin as PermissionRequired
from django.shortcuts import redirect

class PermissionRequiredMixin(PermissionRequired):
    permission_redirect_field_name = "dashboard"

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect("error", next=self.permission_redirect_field_name, msg="没有权限，请联系管理员")
        return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)