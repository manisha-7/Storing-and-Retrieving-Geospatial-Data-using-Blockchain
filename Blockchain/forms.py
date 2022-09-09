from dataclasses import field
from django import forms

from django.db.models import fields
from django.forms import ModelForm
from django.forms.widgets import DateInput
from .models import *
from django.contrib.admin.widgets import  AdminDateWidget, AdminTimeWidget, AdminSplitDateTime

import imp
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class MyfileUploadForm(forms.Form):
    # class Meta:
    #     model= file_upload
    #     fields= '__all__'
    # Coordinate = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # date_time = forms.DateField(widget=forms.DateInput(format='%YYYY-%MM-%DD'), input_formats=['%YYYY-%MM-%DD'])
    # Location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # Satellite = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # type_of_data = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    files_data = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))

   
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']