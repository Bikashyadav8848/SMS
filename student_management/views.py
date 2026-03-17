from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from students.models import Student
from teachers.models import Teacher
from classes.models import Class
from attendance.models import Attendance
from exams.models import Marks

# Home
def home(request):
    return render(request, 'home.html')

# Students
class StudentListView(ListView):
    model = Student
    template_name = 'students.html'
    context_object_name = 'students'

class StudentDetailView(DetailView):
    model = Student
    template_name = 'student_detail.html'

class StudentCreateView(CreateView):
    model = Student
    template_name = 'student_form.html'
    fields = ['name', 'email', 'roll_number']
    success_url = reverse_lazy('students')

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'student_form.html'
    fields = ['name', 'email', 'roll_number']
    success_url = reverse_lazy('students')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_confirm_delete.html'
    success_url = reverse_lazy('students')

# Teachers
class TeacherListView(ListView):
    model = Teacher
    template_name = 'teachers.html'
    context_object_name = 'teachers'

class TeacherCreateView(CreateView):
    model = Teacher
    template_name = 'teacher_form.html'
    fields = ['name', 'subject']
    success_url = reverse_lazy('teachers')

class TeacherUpdateView(UpdateView):
    model = Teacher
    template_name = 'teacher_form.html'
    fields = ['name', 'subject']
    success_url = reverse_lazy('teachers')

class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'teacher_confirm_delete.html'
    success_url = reverse_lazy('teachers')

# Classes
class ClassListView(ListView):
    model = Class
    template_name = 'classes.html'
    context_object_name = 'classes'

class ClassCreateView(CreateView):
    model = Class
    template_name = 'class_form.html'
    fields = ['name', 'section']
    success_url = reverse_lazy('classes')

class ClassUpdateView(UpdateView):
    model = Class
    template_name = 'class_form.html'
    fields = ['name', 'section']
    success_url = reverse_lazy('classes')

class ClassDeleteView(DeleteView):
    model = Class
    template_name = 'class_confirm_delete.html'
    success_url = reverse_lazy('classes')

# Attendance
class AttendanceListView(ListView):
    model = Attendance
    template_name = 'attendance.html'
    context_object_name = 'attendances'

class AttendanceCreateView(CreateView):
    model = Attendance
    template_name = 'attendance_form.html'
    fields = ['student', 'date', 'status']
    success_url = reverse_lazy('attendance')

class AttendanceUpdateView(UpdateView):
    model = Attendance
    template_name = 'attendance_form.html'
    fields = ['student', 'date', 'status']
    success_url = reverse_lazy('attendance')

class AttendanceDeleteView(DeleteView):
    model = Attendance
    template_name = 'attendance_confirm_delete.html'
    success_url = reverse_lazy('attendance')

# Marks
class MarksListView(ListView):
    model = Marks
    template_name = 'marks.html'
    context_object_name = 'marks'

class MarksCreateView(CreateView):
    model = Marks
    template_name = 'marks_form.html'
    fields = ['student', 'subject', 'marks']
    success_url = reverse_lazy('marks')

class MarksUpdateView(UpdateView):
    model = Marks
    template_name = 'marks_form.html'
    fields = ['student', 'subject', 'marks']
    success_url = reverse_lazy('marks')

class MarksDeleteView(DeleteView):
    model = Marks
    template_name = 'marks_confirm_delete.html'
    success_url = reverse_lazy('marks')