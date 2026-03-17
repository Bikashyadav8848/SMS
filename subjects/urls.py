from django.urls import path
from .views import (
    SubjectListView, SubjectDetailView, SubjectCreateView,
    SubjectUpdateView, SubjectDeleteView
)

urlpatterns = [
    path('', SubjectListView.as_view(), name='subjects'),
    path('add/', SubjectCreateView.as_view(), name='subject_add'),
    path('<int:pk>/', SubjectDetailView.as_view(), name='subject_detail'),
    path('<int:pk>/edit/', SubjectUpdateView.as_view(), name='subject_edit'),
    path('<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject_delete'),
]
