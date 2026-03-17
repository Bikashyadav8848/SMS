from rest_framework import serializers
from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'teacher', 'teacher_name', 'description']
