from django import forms
from django.contrib.auth.models import User

class AddUserForm(forms.Form):
    username = forms.CharField(required=True)
    name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    weixin = forms.CharField(required=True)
    password = forms.CharField(required=True)

    # 判断登录用户名中是否已存在
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user_obj = User.objects.get(username=username)
            raise forms.ValidationError("已存在该用户名")
        except User.DoesNotExist:
            return username
    # 判断手机号码是否存在

