from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import User

from .models import Profile

# Register your models here.
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_superuser')
    list_display_links = ('id', 'email')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'test_completed', 'is_assigned', 'is_result')
    list_display_links = ('id', 'full_name')
    list_filter = ('is_assigned', 'is_result')
    search_fields = ('user__first_name', 'user__last_name')