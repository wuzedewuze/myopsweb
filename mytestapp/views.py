from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
class FirstForm(TemplateView):

    template_name = "testform.html"


