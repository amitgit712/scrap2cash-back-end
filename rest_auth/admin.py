from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from rest_auth.models import User,UserProfile,BussinessProfile,PasswordChanged



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','admin_image_link')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'verify_email','is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name','verify_email' ,'admin_image_link','last_name', 'is_staff')
    search_fields = ('email', 'verify_email','first_name', 'admin_image_link','last_name')
    ordering = ('email',)


admin.site.register(UserProfile)
admin.site.register(PasswordChanged)
#admin.site.register(BussinessProfile)
