# Generated by Django 3.2.5 on 2021-07-08 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fakeCSV', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='column',
            options={'ordering': ['column_order']},
        ),
    ]