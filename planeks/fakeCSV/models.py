from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_('Username must be set'))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Schema(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    schema_name = models.CharField(
        null=False,
        blank=False,
        max_length=255,
    )

    date_edit = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.schema_name}"


class Column(models.Model):
    type_choices = (
        ('email', 'EMAIL'),
        ('full name', 'FULL_NAME'),
        # ('job', 'JOB'),
        # ('domain name', 'DOMAIN_NAME'),
        ('phone number', 'PHONE_NUMBER'),
        ('text', 'TEXT'),
        # ('integer', 'INTEGER'),
        # ('address', 'ADDRESS'),
        ('date', 'DATE'),
    )

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    name = models.CharField(
        null=False,
        blank=False,
        max_length=255,
    )

    column_type = models.CharField(
        null=False,
        blank=False,
        choices=type_choices,
        max_length=255
    )

    column_order = models.IntegerField(
        default=0,
    )

    column_from = models.IntegerField(
        null=True,
        blank=True
    )

    column_to = models.IntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.schema} :  {self.name}"


class DataSet(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    date_create = models.DateField(
        auto_now=True,
    )

    file_path = models.CharField(max_length=2500, blank=True, null=True)

    def __str__(self):
        return f"{self.schema}"
