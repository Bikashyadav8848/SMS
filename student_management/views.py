from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from students.models import Student
from teachers.models import Teacher
from classes.models import Class
from attendance.models import Attendance
from exams.models import Marks
from subjects.models import Subject
from timetable.models import TimetableEntry
from fees.models import FeeCategory, FeeStructure, StudentFee, FeePayment
from django.db.models import Sum
from django.contrib import messages
from accounts.models import SystemSettings
from accounts.forms import SystemSettingsForm

# Home
def home(request):
    context = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'total_classes': Class.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_timetable_entries': TimetableEntry.objects.count(),
        'total_fee_categories': FeeCategory.objects.count(),
        'total_fee_structures': FeeStructure.objects.count(),
        'total_student_fees': StudentFee.objects.count(),
        'total_fee_payments': FeePayment.objects.count(),
        'total_fees_assigned': StudentFee.objects.aggregate(total=Sum('total_amount'))['total'] or 0,
        'total_fees_paid': StudentFee.objects.aggregate(total=Sum('paid_amount'))['total'] or 0,
        'total_fees_due': StudentFee.objects.aggregate(total=Sum('due_amount'))['total'] or 0,
    }
    return render(request, 'home.html', context)

# Settings Page
def settings_page(request):
    settings_obj = SystemSettings.get_settings()
    
    if request.method == 'POST':
        form = SystemSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "System settings updated successfully!")
            return redirect('settings')
    else:
        form = SystemSettingsForm(instance=settings_obj)
        
    return render(request, 'settings.html', {'form': form, 'settings': settings_obj})

# Students
class StudentListView(ListView):
    model = Student
    template_name = 'students.html'
    context_object_name = 'students'
    ordering = ['roll_number']

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
    fields = ['teacher_id', 'name', 'email', 'phone', 'subject', 'qualification', 'experience_years']
    success_url = reverse_lazy('teachers')

class TeacherUpdateView(UpdateView):
    model = Teacher
    template_name = 'teacher_form.html'
    fields = ['teacher_id', 'name', 'email', 'phone', 'subject', 'qualification', 'experience_years']
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
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('student')
        
        student_search = self.request.GET.get('student')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if student_search:
            queryset = queryset.filter(student__name__icontains=student_search)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        # Calculate statistics
        context['total_records'] = queryset.count()
        context['present_count'] = queryset.filter(status='Present').count()
        context['absent_count'] = queryset.filter(status='Absent').count()
        context['leave_count'] = queryset.exclude(status__in=['Present', 'Absent']).count()
        
        return context


class AttendanceCreateView(CreateView):
    model = Attendance
    template_name = 'attendance_form.html'
    fields = ['student', 'date', 'status']
    success_url = reverse_lazy('attendance')

    def get_initial(self):
        from django.utils import timezone
        initial = super().get_initial()
        initial['date'] = timezone.now().date()
        return initial

class AttendanceUpdateView(UpdateView):
    model = Attendance
    template_name = 'attendance_form.html'
    fields = ['student', 'date', 'status']
    success_url = reverse_lazy('attendance')

class AttendanceDeleteView(DeleteView):
    model = Attendance
    template_name = 'attendance_confirm_delete.html'
    success_url = reverse_lazy('attendance')

# Bulk Attendance Marking
def bulk_attendance(request):
    """Mark attendance for multiple students at once"""
    from datetime import date
    
    if request.method == 'POST':
        attendance_date = request.POST.get('date')
        present_students = request.POST.getlist('present_students')
        
        if attendance_date:
            # Create/update attendance for present students
            for student_id in present_students:
                try:
                    student = Student.objects.get(id=student_id)
                    Attendance.objects.update_or_create(
                        student=student,
                        date=attendance_date,
                        defaults={'status': 'Present'}
                    )
                except Student.DoesNotExist:
                    pass
        
        return redirect('attendance')
    
    # GET request - show form with all students and today's date
    today = date.today()
    students = Student.objects.all().order_by('name')
    
    context = {
        'students': students,
        'today': today,
    }
    
    return render(request, 'bulk_attendance.html', context)

# Marks
class MarksListView(ListView):
    model = Marks
    template_name = 'marks.html'
    context_object_name = 'marks'

class MarksCreateView(CreateView):
    model = Marks
    template_name = 'marks_form.html'
    fields = ['student', 'subject', 'exam_name', 'marks', 'out_of']
    success_url = reverse_lazy('marks')

class MarksUpdateView(UpdateView):
    model = Marks
    template_name = 'marks_form.html'
    fields = ['student', 'subject', 'exam_name', 'marks', 'out_of']
    success_url = reverse_lazy('marks')

class MarksDeleteView(DeleteView):
    model = Marks
    template_name = 'marks_confirm_delete.html'
    success_url = reverse_lazy('marks')