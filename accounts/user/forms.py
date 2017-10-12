from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile


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
            User.objects.get(username=username)
            raise forms.ValidationError("已存在该用户名")
        except User.DoesNotExist:
            return username

    # 判断手机号码是否存在
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        try:
            Profile.objects.get(phone=phone)
            raise forms.ValidationError("手机号码重复啦")
        except Profile.DoesNotExist:
            return phone
