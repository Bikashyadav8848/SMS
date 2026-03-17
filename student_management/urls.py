STATIC_URL = 'static/'
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserProfileViewSet
from students.views import StudentViewSet
from teachers.views import TeacherViewSet
from classes.views import ClassViewSet
from attendance.views import AttendanceViewSet
from exams.views import MarksViewSet
from . import views
from .admin import admin_site

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'students', StudentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'marks', MarksViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', views.home, name='home'),
    # Students
    path('students/', views.StudentListView.as_view(), name='students'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    # Teachers
    path('teachers/', views.TeacherListView.as_view(), name='teachers'),
    path('teachers/add/', views.TeacherCreateView.as_view(), name='teacher_add'),
    path('teachers/<int:pk>/edit/', views.TeacherUpdateView.as_view(), name='teacher_edit'),
    path('teachers/<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher_delete'),
    # Classes
    path('classes/', views.ClassListView.as_view(), name='classes'),
    path('classes/add/', views.ClassCreateView.as_view(), name='class_add'),
    path('classes/<int:pk>/edit/', views.ClassUpdateView.as_view(), name='class_edit'),
    path('classes/<int:pk>/delete/', views.ClassDeleteView.as_view(), name='class_delete'),
    # Attendance
    path('attendance/', views.AttendanceListView.as_view(), name='attendance'),
    path('attendance/add/', views.AttendanceCreateView.as_view(), name='attendance_add'),
    path('attendance/<int:pk>/edit/', views.AttendanceUpdateView.as_view(), name='attendance_edit'),
    path('attendance/<int:pk>/delete/', views.AttendanceDeleteView.as_view(), name='attendance_delete'),
    # Marks
    path('marks/', views.MarksListView.as_view(), name='marks'),
    path('marks/add/', views.MarksCreateView.as_view(), name='marks_add'),
    path('marks/<int:pk>/edit/', views.MarksUpdateView.as_view(), name='marks_edit'),
    path('marks/<int:pk>/delete/', views.MarksDeleteView.as_view(), name='marks_delete'),
    # Subjects
    path('subjects/', include('subjects.urls')),
]
