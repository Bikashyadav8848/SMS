from rest_framework import viewsets
from .models import Marks
from .serializers import MarksSerializer

class MarksViewSet(viewsets.ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer