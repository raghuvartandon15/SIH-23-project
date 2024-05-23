# Generated by Django 5.0 on 2023-12-19 19:22

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0013_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'Student'), (2, 'Institute'), (3, 'StateAuthority'), (4, 'superuser')], null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('institute_name', models.CharField(max_length=255)),
                ('institute_code', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StateAuthority',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('state_name', models.CharField(max_length=255)),
                ('state_code', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('adhaar', models.CharField(max_length=255)),
                ('scholar_cat', models.CharField(max_length=255)),
                ('dob', models.DateField(default='2000-01-01')),
                ('gender', models.CharField(max_length=10)),
                ('religion', models.CharField(max_length=255)),
                ('category_caste', models.CharField(max_length=255)),
                ('father_name', models.CharField(max_length=255)),
                ('mother_name', models.CharField(max_length=255)),
                ('annual_income', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('phone_number', models.CharField(max_length=15, null=True, unique=True)),
                ('enrollment_no', models.CharField(max_length=20)),
                ('admission_year', models.IntegerField(blank=True, null=True)),
                ('course', models.CharField(blank=True, max_length=255, null=True)),
                ('roll_12', models.CharField(max_length=20)),
                ('board_name_12', models.CharField(blank=True, max_length=255, null=True)),
                ('marks_12', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('roll_10', models.CharField(blank=True, max_length=20, null=True)),
                ('board_name_10', models.CharField(blank=True, max_length=255, null=True)),
                ('marks_10', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('disabled', models.BooleanField(default=False)),
                ('marital_status', models.CharField(blank=True, max_length=20, null=True)),
                ('parents_profession', models.CharField(blank=True, max_length=255, null=True)),
                ('acc_number', models.CharField(max_length=50)),
                ('ifsc_num', models.CharField(max_length=50)),
                ('domicile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.stateauthority')),
                ('institute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.institute')),
            ],
        ),
    ]
