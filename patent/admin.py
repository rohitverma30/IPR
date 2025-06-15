from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import PatentSubmission, Patent, banner_img

User = get_user_model()

@admin.register(PatentSubmission)
class PatentSubmissionAdmin(admin.ModelAdmin):
    list_display = ["name", "surname", "email", "phone", "title", "submitted_at"]
    search_fields = ["name", "surname", "email", "title"]
    list_filter = ["submitted_at"]

@admin.register(Patent)
class PatentAdmin(admin.ModelAdmin):
    list_display = ["name", "surname", "title", "content", "verified_by"]
    search_fields = ["name", "surname", "title"]
    list_filter = ["submitted_at"]

@admin.register(banner_img)
class banner_imgAdmin(admin.ModelAdmin):
    list_display = ["image"]

    def save_model(self, request, obj, form, change):
        """Ensure user exists before saving."""
        if User.objects.filter(id=request.user.id).exists():
            super().save_model(request, obj, form, change)
        else:
            print("Error: Admin user does not exist in the database.")
