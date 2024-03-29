# Generated by Django 3.2.5 on 2021-07-08 11:46

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(max_length=255)),
                ('column_separator', models.CharField(choices=[(',', 'comma'), (';', 'semicolon'), (':', 'colon')], max_length=2)),
                ('string_character', models.CharField(choices=[('"', 'double_quote'), ("'", 'apostrophe')], max_length=2)),
                ('date_edit', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('date_created', models.DateField(auto_now=True)),
                ('file_path', models.CharField(blank=True, max_length=2500, null=True)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fakeCSV.schema')),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=255)),
                ('column_type', models.CharField(choices=[('EMAIL', 'email'), ('FULL_NAME', 'full name'), ('PHONE_NUMBER', 'phone number'), ('TEXT', 'text'), ('INTEGER', 'integer'), ('DATE', 'date')], max_length=255)),
                ('column_order', models.IntegerField(default=0)),
                ('column_from', models.IntegerField(blank=True, default=0, null=True)),
                ('column_to', models.IntegerField(blank=True, null=True)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fakeCSV.schema')),
            ],
        ),
    ]
