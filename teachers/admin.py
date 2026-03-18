from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_id', 'name', 'email', 'phone', 'subject', 'experience_years', 'is_active']
    list_filter = ['is_active', 'subject', 'created_at']
    search_fields = ['name', 'email', 'teacher_id', 'subject']
    readonly_fields = ['created_at', 'updated_at', 'teacher_id']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('teacher_id', 'name', 'email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('subject', 'qualification', 'experience_years')
        }),
        ('System Information', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_editable = ['is_active']
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Mark selected teachers as active"
    
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Mark selected teachers as inactive"