from django.contrib import admin
from .models import StudentProfile,Course,StudentCourses
from .forms import CustomUserChangeForm,CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

admin.site.register(Course)
admin.site.register(StudentCourses)

@admin.register(StudentProfile)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = StudentProfile
    list_display = ("username", "first_name", "last_name",'age','phone', "email")

    fieldsets = UserAdmin.fieldsets + (
        ("Додатковий профіль",
            {'fields': ('age','phone')}
        ),
    )

    add_fieldsets = UserAdmin.fieldsets + (
        (None,
            {'fields': ('age','phone')}
        ),
        
    )
    search_fields = ("username","email","phone")
    ordering = ("username",)

