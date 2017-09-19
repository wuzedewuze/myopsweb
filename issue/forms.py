from django import forms


class CreateIssueForm(forms.Form):
    project_name = forms.CharField(required=True)
    issue_content = forms.CharField(required=True)
    dev_person = forms.CharField(required=True)
    test_person = forms.CharField(required=True)
    issue_person = forms.CharField(required=True)
    svn_path = forms.CharField(required=True)
    remark = forms.CharField(required=False)