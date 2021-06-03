from django.contrib import admin
from .models import UserExtends, Clients
# Register your models here.
@admin.register(UserExtends)
class UserExtendsAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    

