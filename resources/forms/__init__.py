from django import  forms
from resources.models import  Idc

class CreateIdcForm(forms.Form):
    name = forms.CharField(required=True,error_messages={"required":"不能为空值"})
    idc_name =forms.CharField(required=True)
    address = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    email = forms.CharField(required=True)
    username = forms.CharField(required=True)

    # 逐个字段进行验证
    def clean_name(self):
        name = self.cleaned_data.get("name")
        try:
            Idc.objects.get(name__exact=name)
            raise forms.ValidationError("Idc简称 重复啦")
        except Idc.DoesNotExist:
            return name
'''
    # 类验证
    def clean(self):
        data = self.cleaned_data
        return data
'''

class DeleteIdcForm(forms.Form):
    id = forms.CharField(required=True,error_messages={"required":"idc的id不能为空"})

    def clean_id(self):
        id = self.cleaned_data.get("id")
        try:
            Idc.objects.get(id__exact=id)
        except Idc.ObjectDoesNotExist:
            raise forms.ValidationError("要删除的idc信息不存在")
        return id