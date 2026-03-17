
from django.db import models
class Teacher(models.Model):
    name=models.CharField(max_length=100)
    subject=models.CharField(max_length=100)
