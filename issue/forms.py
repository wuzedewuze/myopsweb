from django import forms
from issue.models import IssueRecord
from django.core.exceptions import ObjectDoesNotExist

class CreateIssueForm(forms.Form):
    project_name = forms.CharField(required=True)
    issue_content = forms.CharField(required=True)
    dev_person = forms.CharField(required=True)
    test_person = forms.CharField(required=True)
    issue_person = forms.CharField(required=True)
    svn_path = forms.URLField(required=True,error_messages={"invalid":"必须输入url格式"})
    remark = forms.CharField(required=False)


class ChangeIssueForm(forms.Form):
    id = forms.CharField(required=True,error_messages={"required":"必须输入id"})
    project_name = forms.CharField(required=True)
    issue_content = forms.CharField(required=True)
    dev_person = forms.CharField(required=True)
    test_person = forms.CharField(required=True)
    issue_time = forms.CharField(required=True)
    issue_person = forms.CharField(required=True)
    svn_path = forms.URLField(required=True,error_messages={"invalid":"必须输入url格式"})
    remark = forms.CharField(required=False)

    def clean_id(self):
        id = self.cleaned_data['id']
        try:
            p_obj = IssueRecord.objects.get(id = id)
        except ObjectDoesNotExist:
            raise forms.ValidationError("发布不存在")
        return id


# 删除发布项目验证
class DeleteIssueForm(forms.Form):
    id = forms.CharField(required=True,error_messages={"required":"必须输入id"})
    def clean_id(self):
        id = self.cleaned_data['id']
        try:
            p_obj = IssueRecord.objects.get(id = id)
        except ObjectDoesNotExist:
            raise forms.ValidationError("发布不存在")
        return id


# 修改发布项目状态验证
class ChangeIssueStatuForm(forms.Form):
    id = forms.CharField(required=True,error_messages={"required":"必须输入id"})

    def clean_id(self):
        id = self.cleaned_data['id']
        try:
            p_obj = IssueRecord.objects.get(id = id)
        except ObjectDoesNotExist:
            raise forms.ValidationError("发布不存在")
        return id

