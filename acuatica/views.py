from django.shortcuts import render, redirect
from .forms import LoginForm, CreateUserForm
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'acuatica/acuatica.html')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = request.POST['user']
            password = request.POST['password']
            user = authenticate(username=user, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user, backend=None)
                    return render(request, 'acuatica/acuatica.html')
                else:
                    messages.error(request, 'Usuario inactivo')
            else:
                messages.error(request, 'Usuario o contraseña incorrecto')
    else:
        form = LoginForm()
    return render(request, 'acuatica/index.html', {'form': form})


def register_view(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(
                request, 'Se creo correctamente la cuenta ' + user)

            return redirect('acuatica.login')

    context = {'form': form}
    return render(request, 'acuatica/register.html', context)


def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('acuatica.index')

        else:
            messages.info(request, 'Usuario o contraseña son incorrectos')

    return render(request, 'acuatica/login.html')


def logoutUser(request):
    logout(request)
    messages = "Hasta pronto"
    return redirect('acuatica.login')


def sales(request):
    return render(request, 'acuatica/venta_normal.html')


def clients(request):
    return render(request, 'acuatica/clientes.html')


def catalogo(request):
    return render(request, 'acuatica/catalogo.html')


def inputs(request):
    return render(request, 'acuatica/entradas.html')


def sales_report(request):
    return render(request, 'acuatica/reporte-ventas.html')
