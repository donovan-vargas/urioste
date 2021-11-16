import ast
from datetime import date
from django.shortcuts import render, redirect, resolve_url
from .forms import LoginForm, CreateUserForm, InputsForm, InventarioForm, ClientsForm, InventoryForm
from django.urls import reverse
from .models import Inventario, Inputs, Clients, Sales, InvSales
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.cache import cache
from django.db import transaction
from django.contrib.auth.decorators import login_required, permission_required 


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


def calculate_sales(data):
    total = 0
    for d in data:
        item_subtotal = int(d.get('quantity', 1)) * int(d.get('cost', 0))
        total += item_subtotal
    return total

@login_required(login_url='/acuatica/login/')
def sales(request):
    form = InputsForm()
    inv_form = InventarioForm()
    context = {}
    data = []
    data_sale = f"{request.user.username}_sales_total"
    data = cache.get(data_sale, [])
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        inventario = request.POST.get('inventario')
        model_product = Inventario.objects.filter(
            pk=inventario, total_cuantity__gte=quantity).values('id', 'name', 'cost')
        if model_product.count() > 0:
            product = list(model_product)
            product = product[0]
            product['quantity'] = quantity
            data.append(product)
            cache.set(data_sale, data, 300)
        elif model_product.count() <= 0:
            messages.error(request,"No hay mas inventario de este Producto")
            return redirect(reverse('acuatica.sales'))

    total = calculate_sales(data)
    clients = Clients.objects.all()
    context['form'] = form
    context['inv_form'] = inv_form
    context['products'] = data
    context['total'] = total
    context['clients'] = clients
    return render(request, 'acuatica/venta_normal.html', context)


class SalesView(CreateView):
    model = Inputs
    form_class = InputsForm
    template_name = "acuatica/venta_normal.html"
    success_url = reverse_lazy("acuatica.sales")


@login_required(login_url='/acuatica/login/')
def clients(request):
    form = ClientsForm()
    context = {'form': form}
    if request.method == 'POST':
        pk = request.POST.get("id")
        if pk:
            cli = Clients.objects.get(pk=pk)
            form = ClientsForm(request.POST, instance=cli)
        else:
            form = ClientsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado")
    client = request.GET.get('client')
    if client:
        client = client.split()
        try:
            cli = Clients.objects.get(pk=client[0])
        except Exception as e:
            messages.error(request, "Escoja un usario de la lista")
        else:
            context['cli'] = cli
            context['form'] = ClientsForm(instance=cli)
    clients = Clients.objects.all()
    context['clients'] = clients
    return render(request, 'acuatica/clientes.html', context)


@login_required(login_url='/acuatica/login/')
def catalogo(request):
    form = InventoryForm()
    context = {'form': form}
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            cli = Inventario.objects.get(pk=pk)
            form = InventoryForm(request.POST, instance=cli)            
            if form.is_valid():
                form.save()
                messages.success(request, "Prodcuto actualizado")
    inventory = request.GET.get('inventory')
    if inventory:

        try:
            inv = Inventario.objects.get(name=inventory)

        except Exception as e:
            messages.error(request, "Escoja un producto de la lista")
        else:
            context['inv'] = inv
            context['form'] = InventoryForm(instance=inv)

    inventorys = Inventario.objects.all()
    context['inventory'] = inventorys
    return render(request, 'acuatica/catalogo.html', context)


@login_required(login_url='/acuatica/login/')
def inputs(request):
    context = {}
    data = []
    context['inv'] = Inventario.objects.all().values('name', 'id')
    cache_data = f"{request.user.username}_inputs"
    if request.method == 'GET':
        id = request.GET.get('product', "0 0")
        data = cache.get(cache_data, [])
        try:
            id = int(id.split()[0])
        except Exception as e:
            messages.error(request, "Revise los datos")
        else:
            model_product = Inventario.objects.filter(
                pk=id).values('id', 'name', 'cost')
            if model_product.count() > 0:
                product = list(model_product)
                product = product[0]
                product['quantity'] = request.GET.get("quantity", 1)
                data.append(product)
                cache.set(cache_data, data, 300)
    if request.method == "POST":
        data_table = request.POST.get('data')
        data_table = ast.literal_eval(data_table)
        for d in data_table:
            Inputs(
                inventario=Inventario.objects.get(id=d['id']),
                cuantity=d['quantity'],
                comments='',
                sale=0
            ).save()
        cache.delete(cache_data)
        messages.success(request, "Entrada creada")
    context['data_table'] = data

    #jefesito = request.user

    #if jefesito.has_perm('acuatica.is_admin'):
    return render(request, 'acuatica/entradas.html', context)
    #elif jefesito.has_perm('acuatica.is_cashier'):
        #messages.error(request,'Tienes que ser administrador para realizar Entradas :)')
        #return redirect(reverse('acuatica.index'))


@login_required(login_url='/acuatica/login/')
#@permission_required('acuatica.is_admin')
def sales_report(request):
    context = {}
    fechahoy = date.today()
    # sales_report = Sales.objects.filter(created = date.today())
    
    
        
    if request.method == 'GET':
        total = Sales.objects.filter(created = date.today(), status = 'T').aggregate(Sum('total'))
        sales_report = Sales.objects.filter(created=date.today())
    if request.method == "POST":
        client = request.POST.get('client')
        status = request.POST.get('status')
        user = request.POST.get('user')
        init_date = request.POST.get('init_date')
        end_date = request.POST.get('end_date')
        folio = request.POST.get('folio')
        query = Q()
        if client:
            query &= Q(client=client)
        if status:
            query &= Q(status=status)
        if user:
            query &= Q(user=user)
        if init_date and end_date:
            query &= Q(created__gte=init_date)
            query &= Q(created__lte=end_date)
        elif init_date:
            query &= Q(created=init_date)
        if folio:
            query &= Q(pk=folio)

        sales_report = Sales.objects.filter(query)
        total = Sales.objects.filter(query).aggregate(Sum('total'))

    context['total'] = total
    context['sales'] = sales_report

    eljefesito  = request.user
    
    
        
    return render(request, 'acuatica/reporte-ventas.html', context)

    




@login_required(login_url='/acuatica/login/')
def inv_save(request):
    form = InputsForm()
    inv_form = InventarioForm()
    context = {'form': form, 'inv_form': inv_form}
    if request.method == 'POST':
        form = InventarioForm(request.POST, request.FILES)
        if form.is_valid():
            inv = form.save()
            total_cuantity = request.POST.get('total_cuantity')
            inp = Inputs()
            inp.inventario = inv
            inp.cuantity = total_cuantity
            inp.date = date.today()
            inp.sale = 0
            inp.comments = ''
            inp.save()
            messages.success(request, 'Guardado')
        else:
            messages.error(request, 'Ocurrio un error')
    return render(request, 'acuatica/venta_normal.html', context)


@login_required(login_url='/acuatica/login/')
@transaction.atomic
def sales_charge(request):
    data_sale = f"{request.user.username}_sales_total"
    if request.method == 'POST':
        try:
            cash = int(request.POST.get('cash'))
            total = int(request.POST.get('total'))
            items = request.POST.getlist('inv')
            client = request.POST.get('client')
            payForm = request.POST.get('pago')
            comments = request.POST.get('comments')
            client = client.split()
            cli = Clients.objects.get(pk=client[0])
        except Exception as e:
            messages.error(
                request, "Algo salio mal valide los datos y vuelva a intentar")
            return redirect('acuatica.sales')
        if cash < total:
            messages.error(request, "Debe ser mayor al total de la compra")
        elif total <= 0:
            messages.error(request, "Nada que cobrar")
        else:
            sales = Sales()
            sales.user = request.user
            sales.cash = cash
            sales.client = cli
            sales.total = total
            sales.payForm = payForm
            sales.comments = comments
            sales.save()
            for item in items:
                x = item.split(',')
                inv_sales = InvSales()
                inv_sales.user = request.user
                inv_sales.sales = sales
                inv_sales.inventory = Inventario.objects.get(pk=x[0])
                inv_sales.quantity = x[1]
                inv_sales.save()
                inputs = Inputs()
                inputs.inventario = Inventario.objects.get(pk=x[0])
                inputs.cuantity = 0
                inputs.sale = x[1]
                inputs.comments = ''
                inputs.payForm = ''
                inputs.save()
            cache.delete(data_sale)
            messages.success(request, "Venta cobrada")
    return redirect('acuatica.sales')


@login_required(login_url='/acuatica/login/')
def ticket(request):
    context = {}
    sales_user = Sales.objects.all()[Sales.objects.count()-1]
    inv_sale = InvSales.objects.filter(sales=sales_user.pk)
    context['sales'] = sales_user
    context['invSales'] = inv_sale
    return render(request, "ticket.html", context)



@login_required(login_url='/acuatica/login/')
#@permission_required('acuatica.is_admin')
def cancel_sale(request,pk):
    user = request.user
    if user.has_perm('acuatica.is_admin'):
        sales = Sales.objects.get(pk=pk)
        sales.status = 'C'
        
        sales.save()
        messages.success(request, "Venta Cancelada")
        return redirect('acuatica.sales-report')
    elif user.has_perm('acuatica.is_cashier'):
        messages.error(request,"Tienes que ser administrador para esta acción")
        return redirect(reverse('acuatica.sales-report'))