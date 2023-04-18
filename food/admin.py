from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from food import models

# class OwnerAdmin(BaseUserAdmin):
#     """Define the admin pages for users."""
#     ordering = ['_id']
#     list_display = ['email']
#     fieldsets = (
#         (None, {'fields':('email','password')}),
#         (
#             _('Permissions'),
#             {
#                 'fields':(
#                         'is_active',
#                         'is_staff',
#                         'is_superuser'
#                 )
#             }

#         ),
#         ({'fields':('last_login',)}),
#     )
#     readonly_fields = ['last_login']
#     add_fieldsets = (
#         (None, {
#             'classes':('wide',),
#             'fields':(
#                 'email',
#                 'password',
#                 'is_active',
#                 'is_staff',
#                 'is_superuser',
#             )
#         }),
#     )

admin.site.register(models.Owner)
admin.site.register(models.Manager)

