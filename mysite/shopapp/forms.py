from django.shortcuts import (render,redirect,reverse,get_object_or_404,)
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from timeit import default_timer
from django.contrib.auth.models import Group,User
from django.views import View
from django import forms
from django.core import validators


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name',]

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()        