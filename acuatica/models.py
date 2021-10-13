from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _


class UserExtends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_extend', verbose_name='usuario')
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)

    class Meta(object):
        verbose_name_plural = 'Usuario'
        permissions = {
            ('is_cashier', _('Es cajero')),
            ('is_admin', _('Es admin')),
        }

    def __str__(self):
        return str(self.name)


class Levels(models.Model):
    level = models.CharField(max_length=100)

    def __str__(self):
        return str(self.level)


class Clients(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICE = (
        (MALE, 'Hombre'),
        (FEMALE, 'Mujer')
    )

    SINGLE = 'S'
    MARRIED = 'M'
    DIVORCE = 'D'
    FREE = 'F'
    CIVIL_CHOICE = (
        (SINGLE, 'Soltero'),
        (MARRIED, 'Casado'),
        (DIVORCE, 'Divorsiado'),
        (FREE, 'Union libre')
    )

    FACEBOOK = 'F'
    RECOMANDATION = 'R'
    TRANSIT = 'T'
    OTHER = 'F'
    FIND_CHOICES = (
        (FACEBOOK, 'Facebook'),
        (RECOMANDATION, 'Recomendacion'),
        (TRANSIT, 'Transito'),
        (OTHER, 'Otro')
    )

    name = models.CharField(max_length=50)
    #picture = models.ImageField(verbose_name='foto', null=True, blank=True)
    image_source = models.TextField()
    last_name = models.CharField(max_length=50)
    second_last_name = models.CharField(max_length=50)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=SEX_CHOICE, max_length=10)
    address = models.CharField(max_length=200)
    suburb = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    cel = models.CharField(max_length=12)
    email = models.EmailField(blank=True, null=True)
    civil_status = models.CharField(max_length=10, choices=CIVIL_CHOICE)
    heard_from = models.CharField(max_length=10, choices=FIND_CHOICES)
    blood = models.CharField(max_length=50)
    emergency_contact = models.CharField(max_length=200)
    emergency_phone = models.CharField(max_length=20)
    pay_day = models.CharField(max_length=200)
    medical_condition = models.TextField()
    schedule = models.TextField()
    level = models.ForeignKey(Levels, on_delete=models.DO_NOTHING)

    class Meta(object):
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return str(self.name)


class Inventario(models.Model):
    BIG = 'B'
    MEDIUM = 'M'
    SMALL = 'S'
    SIZE_CHOICE = (
        (BIG, 'Grande'),
        (MEDIUM, 'Mediano'),
        (SMALL, 'Chico'),

    )

    ACUATICA = 'A'
    AJUSTES_CONTABLES = 'AJ'
    MANTENIMIENTO = 'M'
    TIENDITA = 'T'
    BRANCH_CHOICES = (
        (ACUATICA, 'Acuatica Urioste'),
        (AJUSTES_CONTABLES, 'Ajustes Contables'),
        (MANTENIMIENTO, 'Mantenimineto'),
        (TIENDITA, 'Tiendita'),
    )

    numcode = models.CharField(max_length=100)
    # categoria A
    # categoria B
    name = models.CharField(max_length=100, unique=True)
    visible = models.BooleanField(default=True)
    size = models.CharField(max_length=20, choices=SIZE_CHOICE, default="0000")
    measures = models.CharField(
        max_length=200, default="medidas para algunos productos")
    # descripcion cuadro bien complejo, creo que seria mejor hacerlo en el front end
    short_name = models.CharField(max_length=60)
    branches = MultiSelectField(
        choices=BRANCH_CHOICES, blank=True, null=True, default=True)
    limited_inventory = models.BooleanField(default=True)
    contained_products = models.CharField(
        max_length=50, default="ProductosContenidos")
    minimum_amount = models.CharField(max_length=200)
    max_amount = models.CharField(max_length=100)
    colors = models.CharField(max_length=100, default="colores")
    browserdescription = models.CharField(
        max_length=100, default="descripcionBuscador")
    browserTitle = models.CharField(max_length=50, default="tituloBrowser")
    friendly_url = models.CharField(max_length=100, default="url")
    cost = models.IntegerField(default=0)
    total_cuantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='images/', blank=True, null=True)

    class Meta(object):
        verbose_name_plural = 'Inventario'

    def __str__(self):
        return self.name


class Inputs(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.DO_NOTHING)
    cuantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    sale = models.IntegerField()
    comments = models.TextField()

    class Meta(object):
        verbose_name_plural = 'Entradas y Salidas'

    def __str__(self):
        return self.inventario.name


def update_total_cuantity(sender, instance, **kwargs):
    count = instance.inventario.inputs_set.all().aggregate(Sum("cuantity"))
    instance.inventario.total_cuantity = count.get('cuantity__sum')
    instance.inventario.save()


def update_total_cuantity_sale(sender, instance, **kwargs):
    count = instance.inventario.inputs_set.all().aggregate(Sum("sale"))
    instance.inventario.total_cuantity -= count.get('sale__sum')
    instance.inventario.save()


post_save.connect(update_total_cuantity, sender=Inputs)
post_delete.connect(update_total_cuantity, sender=Inputs)
post_save.connect(update_total_cuantity_sale, sender=Inputs)
post_delete.connect(update_total_cuantity_sale, sender=Inputs)


class Sales(models.Model):
    TERMINADO = 'T'
    CANCELADO = 'C'
    STATUS_CHOICE = (
        (TERMINADO, 'Terminado'),
        (CANCELADO, 'Cancelado'),
    )
    user = models.ForeignKey(User, related_name='cajero',
                             on_delete=models.DO_NOTHING)
    client = models.ForeignKey(Clients, on_delete=models.DO_NOTHING)
    cash = models.FloatField()
    total = models.FloatField()
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICE, default=TERMINADO)
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return self.user.username


class InvSales(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    inventory = models.ForeignKey(Inventario, on_delete=models.DO_NOTHING)
    sales = models.ForeignKey(Sales, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Cobros'

    def __str__(self):
        return self.user.username
