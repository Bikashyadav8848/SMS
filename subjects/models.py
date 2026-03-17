from django.db import models
from teachers.models import Teacher

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return f"{self.name} - {self.teacher.name}"
