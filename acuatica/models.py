from django.db import models
from django.contrib.auth.models import User

class UserExtends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_extend', verbose_name='usuario')
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)    
    is_admin = models.BooleanField(default=False)

    class Meta(object):
        verbose_name_plural = 'Usuario'

    def __str__(self):
        return str(self.name)

class Levels(models.Model):
    level = models.CharField(max_length=100)


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
    last_name = models.CharField(max_length=50)
    second_last_name = models.CharField(max_length=50)
    birth_date = models.DateField(blank=True)
    gender = models.CharField(choices=SEX_CHOICE, max_length=10)
    address = models.CharField(max_length=200)
    suburb = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    cel = models.CharField(max_length=12)
    email = models.EmailField(blank=True)
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

    



