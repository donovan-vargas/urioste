# coding: utf-8
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime
from acuatica.models import Inventario, Inputs, Clients
from django.contrib.auth.forms import UserCreationForm


class StylishForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    password = forms.CharField(label='Contraseña',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Contraseña'}))


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class InputsForm(forms.ModelForm):
    class Meta:
        model = Inputs
        fields = ('inventario',)
        widgets = {
            'inventario': AutocompleteSelect(
                Inputs._meta.get_field('inventario').remote_field,
                admin.site,
                attrs={'placeholder': 'Seleccionar...', 'class': 'form-control'},
            )
        }

class InventarioForm(forms.ModelForm):

    class Meta:
        model = Inventario
        fields = '__all__'


class ClientsForm(StylishForm):

    class Meta:
        model = Clients
        fields = '__all__'