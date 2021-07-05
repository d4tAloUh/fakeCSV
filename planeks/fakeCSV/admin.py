from django.contrib import admin
from .models import CustomUser, Schema, Column, DataSet

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(DataSet)
