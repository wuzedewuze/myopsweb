from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label="your name",max_length=100)


    def clean_your_name(self):
        your_name = self.cleaned_data['your_name']
        return your_name