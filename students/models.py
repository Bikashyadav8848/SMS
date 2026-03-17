
from django.db import models

class Student(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    roll_number=models.CharField(max_length=20)

    def __str__(self):
        return self.name
