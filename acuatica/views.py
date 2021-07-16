from django.shortcuts import render, redirect
from .forms import InputsForm, LoginForm, CreateUserForm, InputsForm
from django.urls import reverse
from .models import Inventario, Inputs, Clients
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
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
    form = InputsForm()
    context = {}
    if request.method == 'POST':        
        quantity = request.POST.get('quantity', 1)
        inventario = request.POST.get('inventario')
        client = request.POST.get('client')
        model_product = Inventario.objects.filter(pk=inventario, total_cuantity__gte=0)
        context['quantity'] = quantity
        context['products'] = model_product
    context['form'] = form
    return render(request, 'acuatica/venta_normal.html', context)

class SalesView(CreateView):
    model = Inputs    
    form_class = InputsForm
    template_name = "acuatica/venta_normal.html"
    success_url = reverse_lazy("acuatica.sales")


def clients(request):
    context = {}
    if request.method == 'GET':
        clients = Clients.objects.all()
        context['clients'] = clients
    if request.method == 'POST':
        name = request.POST.get('name')
        clients = Clients.objects.filter(name__contains=name)
        context['clients'] = clients
    return render(request, 'acuatica/clientes.html', context)


def catalogo(request):
    return render(request, 'acuatica/catalogo.html')


def inputs(request):
    return render(request, 'acuatica/entradas.html')


def sales_report(request):
    return render(request, 'acuatica/reporte-ventas.html')
