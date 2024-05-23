


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Student, Institute, StateAuthority
from .models import CustomUser, Student, Institute, StateAuthority,ScholarCategory
from scholar.models import Docs

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ['username','first_name','last_name', 'email', 'user_type','password', 'is_staff', 'is_active']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'user_type')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


class StudentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Student._meta.fields]

class StudentInline(admin.StackedInline):  # or admin.TabularInline
    model = Student

class InstituteAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Institute._meta.fields]
    
    def save_model(self, request, obj, form, change):
        # Save the Institute instance
        super().save_model(request, obj, form, change)

        # Check if the user is already assigned
        if not obj.user:
            # Assign the current user to the Institute's user field
            user = CustomUser.objects.create_user(username=obj.institute_code, user_type=2)  # Set user_type to Institute (2)
            obj.user = user
            obj.save()

class StateAuthorityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in StateAuthority._meta.fields]

    def save_model(self, request, obj, form, change):
        # Save the StateAuthority instance
        super().save_model(request, obj, form, change)

        # Check if the user is already assigned
        if not obj.user:
            # Assign the current user to the StateAuthority's user field
            user = CustomUser.objects.create_user(username=obj.state_code, user_type=3)  # Set user_type to StateAuthority (3)
            obj.user = user
            obj.save()

# Register CustomUser with the BaseUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(StateAuthority, StateAuthorityAdmin)

admin.site.register(ScholarCategory)
admin.site.register(Docs)


