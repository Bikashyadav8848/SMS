from django.contrib import admin
from .models import Marks

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'marks']