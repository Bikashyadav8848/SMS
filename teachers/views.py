from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Teacher
from .serializers import TeacherSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teachers.
    Provides CRUD operations with filtering and search capabilities.
    """
    queryset = Teacher.objects.filter(is_active=True).order_by('name')
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['subject', 'is_active']
    search_fields = ['name', 'email', 'teacher_id', 'subject']
    ordering_fields = ['name', 'created_at', 'experience_years']
    
    def perform_create(self, serializer):
        """Generate unique teacher ID on creation"""
        teacher = serializer.save()
        if not teacher.teacher_id or teacher.teacher_id == 'TCH':
            teacher.teacher_id = f"TCH{teacher.id:04d}"
            teacher.save()
    
    @action(detail=False, methods=['get'])
    def active_teachers(self, request):
        """Get all active teachers"""
        teachers = Teacher.objects.filter(is_active=True)
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a teacher"""
        teacher = self.get_object()
        teacher.is_active = False
        teacher.save()
        return Response({'status': 'Teacher deactivated'})
    
    @action(detail=False, methods=['get'])
    def by_subject(self, request):
        """Get teachers by subject"""
        subject = request.query_params.get('subject')
        if not subject:
            return Response({'error': 'Subject parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        teachers = Teacher.objects.filter(subject=subject, is_active=True)
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)