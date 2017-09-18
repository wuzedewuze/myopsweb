from django import forms 
from django.contrib.auth.models import Group

class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={"required":"请输入账号"})
    password = forms.CharField(required=True,error_messages={"required":"请输入密码"})

    
class CreatePermissionForm(forms.Form):
    content_type_id = forms.IntegerField(required=True)
    codename = forms.CharField(required=True)
    name = forms.CharField(required=True)

    def clean_content_type_id(self):
        content_type_id = self.cleaned_data.get("content_type_id")
        return content_type_id

    def clean_codename(self):
        codename = self.cleaned_data.get("codename")
        # 中间不可以有空格
        if codename.find(" "):
            raise forms.ValidationError("不可以有空格")
        else:
            return codename


class GroupForm(forms.Form):
    name = forms.CharField(required=True,error_messages={"required":"组名不能为空"})
    def clean_name(self):
        name = self.cleaned_data.get("name")
        try:
            group = Group.objects.get(name__exact=name)
        except Group.DoesNotExist:
            raise forms.ValidationError("用户组不存在")
        except Exception as e:
            raise forms.ValidationError("验证获取用户组发现"+e+"异常")
        if group.permissions.all():
            raise forms.ValidationError("组内部不可以有权限")
        elif group.user_set.all():
            raise forms.ValidationError("组内部不可以有用户")
        return name
