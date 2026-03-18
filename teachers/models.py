
from django.db import models
from django.core.validators import EmailValidator, RegexValidator

class Teacher(models.Model):
    # Personal Information
    teacher_id = models.CharField(max_length=20, unique=True, default='TCH')
    name = models.CharField(max_length=100, help_text="Teacher's full name")
    email = models.EmailField(unique=True, validators=[EmailValidator()], help_text="Unique email address")
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^[0-9]{10}$', 'Phone must be 10 digits')],
        help_text="10-digit phone number"
    )
    
    # Professional Information
    subject = models.CharField(max_length=100, help_text="Subject taught by teacher")
    qualification = models.CharField(max_length=100, blank=True, help_text="Educational qualification")
    experience_years = models.IntegerField(default=0, help_text="Years of teaching experience")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ['name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['teacher_id']),
        ]

    def __str__(self):
        return f"{self.name} ({self.subject})"
    
    @property
    def display_name(self):
        return f"{self.name} - {self.subject}"
