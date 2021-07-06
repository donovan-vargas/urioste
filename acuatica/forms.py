# coding: utf-8
from django import forms
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    user = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    password = forms.CharField(label='Contraseña',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Contraseña'}))


# def login_view(request):
#    if request.user.is_authenticated:
#        return render(request, 'acuatica/acuatica.html')
#    if request.method == "POST":
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            user = request.POST['user']
#            user = authenticate(username=user, password=password)
#            password = request.POST['password']
#            if user is not None:
#                if user.is_active:
#                    login(request, user, backend=None)
#                    return render(request, 'acuatica/acuatica.html')
#                else:
#                    messages.error(request, 'Usuario inactivo')
#           else:
#                messages.error(request, 'Usuario o contraseña incorrecto')
#    else:
#        form = LoginForm()
#    return render(request, 'acuatica/loginrepuesto.html', {'form': form})

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
