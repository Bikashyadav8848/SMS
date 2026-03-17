from django.contrib import admin
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'created_at']
    list_filter = ['teacher', 'created_at']
    search_fields = ['name', 'teacher__name']
    ordering = ['-created_at']
