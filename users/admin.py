# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from users.models import User

# class CustomUserAdmin(UserAdmin):
#     model = User
#     list_display = ('email', 'first_name', 'last_name', 'is_active')
#     list_filter = ('is_staff', 'is_superuser')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('first_name', 'last_name', 'address', 'phone_number')}),
#         ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
#         ('Important Dates', {'fields': ('date_joined', 'last_login')})
#     )

#     add_fieldsets = (
#         (None, {
#             'classes':('wide',),
#             'fields':('email', 'password1', 'password2', 'is_active', 'is_staff')
#         })
#     )

#     search_fields = ('email',)
#     ordering = ('email',)

# admin.site.register(User, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
