from django.contrib import admin
from .models import UserExtends, Clients, Inventario, Inputs, Levels, Sales, InvSales
# Register your models here.
@admin.register(UserExtends)
class UserExtendsAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
   search_fields = ('name'),
   list_display = ('name',)

@admin.register(Inputs)
class InputsAdmin(admin.ModelAdmin):
    list_display = ('inventario',)
    autocomplete_fields = ('inventario',)


@admin.register(Levels)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('level',)
    

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ('user', 'client', 'cash', 'total', 'created')

@admin.register(InvSales)
class InvSalesAdmin(admin.ModelAdmin):
    list_display = ('user', 'inventory', 'sales', 'quantity')