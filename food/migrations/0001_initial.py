# Generated by Django 4.1.8 on 2023-05-05 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('contact_number', models.IntegerField(default=None)),
                ('role', models.CharField(choices=[('customer', 'customer'), ('manager', 'manager'), ('owner', 'owner')], default='customer', max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill', models.FloatField()),
                ('status', models.CharField(default='Waiting', max_length=255)),
                ('jrnl_no', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('bill_amt', models.IntegerField(blank=True, default=None, null=True)),
                ('payment_status', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('screenshot', models.ImageField(blank=True, default=None, null=True, upload_to='payment')),
                ('order_date', models.DateTimeField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(default=None, max_length=255)),
                ('image', models.ImageField(upload_to='images')),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(default=None, max_length=255)),
                ('quantity', models.IntegerField()),
                ('image', models.ImageField(upload_to='orders')),
                ('price', models.IntegerField()),
                ('basket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.basket')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('menu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food.menuitems')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.TextField(max_length=255)),
                ('broadcast_on', models.DateTimeField()),
                ('is_seen', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-broadcast_on'],
            },
        ),
    ]
