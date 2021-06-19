# coding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime


class LoginForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    password = forms.CharField(label='Contraseña',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Contraseña'}))
