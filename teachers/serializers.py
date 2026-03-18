from rest_framework import serializers
from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Teacher
        fields = ['id', 'teacher_id', 'name', 'email', 'phone', 'subject', 
                  'qualification', 'experience_years', 'is_active', 
                  'display_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'teacher_id']
        extra_kwargs = {
            'email': {'required': True},
            'phone': {'required': True},
            'subject': {'required': True},
        }
    
    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError("Experience years cannot be negative")
        if value > 70:
            raise serializers.ValidationError("Experience years seems unrealistic")
        return value
    
    def get_display_name(self, obj):
        return obj.display_name