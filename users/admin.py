from django.contrib import admin
from .models import TeamMember
from .models import SlideshowImage
from .models import Blog
from .models import InternEmail, StaffEmail, Pass_key
from .models import News
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

admin.site.register(News)
admin.site.register(InternEmail)
admin.site.register(StaffEmail)
admin.site.register(Pass_key)

@admin.register(User)
class CustomUserAdmin(UserAdmin):  # Ensures compatibility with Django admin
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role',)}),  # Add your custom fields
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'role')



admin.site.register(TeamMember)

@admin.register(SlideshowImage)
class SlideshowImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'uploaded_at')  
    ordering = ('order',)  



class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'content','last_edited_at', 'is_edited']
    ordering = ['-created_at']

admin.site.register(Blog, BlogAdmin)

