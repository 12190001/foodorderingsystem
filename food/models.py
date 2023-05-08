# from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from djongo import models
from django.contrib.auth.hashers import make_password

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """create and return a new supeAruser"""
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    _id = models.ObjectIdField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    contact_number = models.IntegerField(default = None)
    ROLE_CHOICES = [
        ('customer', 'customer'),
        ('manager', 'manager'),
        ('owner', 'owner')
    ]
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='customer')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email" #field used for authentication

class MenuItems(models.Model):
    manager_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, default=None)
    image = models.ImageField(upload_to = 'images')
    description = models.TextField()
    price = models.IntegerField()

class Basket(models.Model):
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bill = models.FloatField()
    STATUS_CHOICES = [
        ('Waiting','Waiting'),
        ('In_progress', 'In_progress'),
        ('Ready', 'Ready'),
        ('Declined', 'Declined'),
        ('Completed','Completed'),
        ('Cancel','Cancel')
    ]
    status = models.CharField(max_length=255, default='Waiting')
    jrnl_no = models.CharField(max_length=255,null=True, blank=True, default=None)
    bill_amt = models.IntegerField(null=True, blank=True, default=None)
    STATUS_CHOICES = [
        ('paid_by_cash', 'cash'),
        ('paid_by_online', 'online'),
    ]
    payment_status = models.CharField(max_length=255,null=True, blank=True, default=None)
    screenshot = models.ImageField(upload_to = 'payment', null=True, blank=True, default=None)
    order_date = models.DateTimeField()

class OrderItems(models.Model):
    basket_id = models.ForeignKey(Basket,on_delete=models.CASCADE)
    menu_id = models.ForeignKey(MenuItems,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255, default=None)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to = 'orders')
    price = models.IntegerField()


class Notification(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification = models.TextField(max_length=255)
    broadcast_on = models.DateTimeField()
    is_seen = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']

    def save(self, *args, **kwars):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("notification", {
        "type": "notify_manager",
        "message": f"New food request: {self.notification}",
        })
        # channel_layer = get_channel_layer()
        # print('saved')
        # notification_objs = 4
        # data = {'count':notification_objs, 'current_notification':self.notification}
        # async_to_sync(channel_layer.group_send)(
        #     'test_consumer_group', {
        #         'type':'send_notification',
        #         'value':json.dumps(data)
        #     }
        # )
        super(Notification, self).save(*args, **kwars)





