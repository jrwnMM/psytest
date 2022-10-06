from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.models import User

from .models import Profile,EducationLevel,Program,Year, Department

# Register your models here.
admin.site.unregister(User)

admin.site.register(EducationLevel)
admin.site.register(Year)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_superuser')
    list_display_links = ('id', 'email')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name','year','program','department', 'last_test_taken', 'is_assigned')
    list_display_links = ('id', 'full_name')
    list_filter = ('is_assigned', 'gender', 'educationlevel', 'department', 'program')
    search_fields = ('user__first_name', 'user__last_name')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code','name')

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id','department', 'name')

