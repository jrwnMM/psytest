from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import User

from .models import Profile,Department,Program,Year

# Register your models here.
admin.site.unregister(User)

admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Year)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_superuser')
    list_display_links = ('id', 'email')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name','year','program','department', 'test_completed', 'is_assigned', 'is_result')
    list_display_links = ('id', 'full_name')
    list_filter = ('is_assigned', 'is_result')
    search_fields = ('user__first_name', 'user__last_name')


