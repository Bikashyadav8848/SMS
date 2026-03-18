from datetime import date
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from django.contrib import messages
from .models import FeeCategory, FeeStructure, StudentFee, FeePayment
from students.models import Student
from classes.models import Class

# Fee Category Views
class FeeCategoryListView(ListView):
    model = FeeCategory
    template_name = 'fee_categories.html'
    context_object_name = 'fee_categories'
    paginate_by = 10

class FeeCategoryCreateView(CreateView):
    model = FeeCategory
    template_name = 'fee_category_form.html'
    fields = ['name', 'description', 'is_active']
    success_url = reverse_lazy('fee_categories')

class FeeCategoryUpdateView(UpdateView):
    model = FeeCategory
    template_name = 'fee_category_form.html'
    fields = ['name', 'description', 'is_active']
    success_url = reverse_lazy('fee_categories')

class FeeCategoryDeleteView(DeleteView):
    model = FeeCategory
    template_name = 'fee_category_confirm_delete.html'
    success_url = reverse_lazy('fee_categories')

# Fee Structure Views
class FeeStructureListView(ListView):
    model = FeeStructure
    template_name = 'fee_structures.html'
    context_object_name = 'fee_structures'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        class_id = self.request.GET.get('class')
        category_id = self.request.GET.get('category')
        if class_id:
            queryset = queryset.filter(class_section_id=class_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = Class.objects.all()
        context['categories'] = FeeCategory.objects.filter(is_active=True)
        return context

class FeeStructureCreateView(CreateView):
    model = FeeStructure
    template_name = 'fee_structure_form.html'
    fields = ['name', 'category', 'class_section', 'fee_type', 'amount', 'frequency', 'due_date', 'is_active']
    success_url = reverse_lazy('fee_structures')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_exist'] = FeeCategory.objects.exists()
        return context

class FeeStructureUpdateView(UpdateView):
    model = FeeStructure
    template_name = 'fee_structure_form.html'
    fields = ['name', 'category', 'class_section', 'fee_type', 'amount', 'frequency', 'due_date', 'is_active']
    success_url = reverse_lazy('fee_structures')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_exist'] = FeeCategory.objects.exists()
        return context

class FeeStructureDeleteView(DeleteView):
    model = FeeStructure
    template_name = 'fee_structure_confirm_delete.html'
    success_url = reverse_lazy('fee_structures')

# Student Fee Views
class StudentFeeListView(ListView):
    model = StudentFee
    template_name = 'student_fees.html'
    context_object_name = 'student_fees'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('student', 'fee_structure', 'fee_structure__category', 'fee_structure__class_section')
        student_id = self.request.GET.get('student')
        class_id = self.request.GET.get('class')
        status = self.request.GET.get('status')
        academic_year = self.request.GET.get('academic_year')

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if class_id:
            queryset = queryset.filter(fee_structure__class_section_id=class_id)
        if status:
            queryset = queryset.filter(status=status)
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()
        context['classes'] = Class.objects.all()
        context['status_choices'] = StudentFee.STATUS_CHOICES
        context['academic_years'] = StudentFee.objects.values_list('academic_year', flat=True).distinct()

        # Calculate totals
        queryset = self.get_queryset()
        context['total_fees'] = queryset.aggregate(total=Sum('total_amount'))['total'] or 0
        context['total_paid'] = queryset.aggregate(total=Sum('paid_amount'))['total'] or 0
        context['total_due'] = queryset.aggregate(total=Sum('due_amount'))['total'] or 0

        return context

class StudentFeeCreateView(CreateView):
    model = StudentFee
    template_name = 'student_fee_form.html'
    fields = ['student', 'fee_structure', 'academic_year', 'total_amount', 'status']
    success_url = reverse_lazy('student_fees')

class StudentFeeUpdateView(UpdateView):
    model = StudentFee
    template_name = 'student_fee_form.html'
    fields = ['student', 'fee_structure', 'academic_year', 'total_amount', 'status']
    success_url = reverse_lazy('student_fees')

class StudentFeeDeleteView(DeleteView):
    model = StudentFee
    template_name = 'student_fee_confirm_delete.html'
    success_url = reverse_lazy('student_fees')

# Fee Payment Views
class FeePaymentListView(ListView):
    model = FeePayment
    template_name = 'fee_payments.html'
    context_object_name = 'fee_payments'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('student_fee', 'student_fee__student', 'student_fee__fee_structure')
        student_id = self.request.GET.get('student')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        if student_id:
            queryset = queryset.filter(student_fee__student_id=student_id)
        if date_from:
            queryset = queryset.filter(payment_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(payment_date__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['students'] = Student.objects.all()

        # Calculate payment totals
        queryset = self.get_queryset()
        context['total_payments'] = queryset.aggregate(total=Sum('amount'))['total'] or 0

        return context

class FeePaymentCreateView(CreateView):
    model = FeePayment
    template_name = 'fee_payment_form.html'
    fields = ['student_fee', 'amount', 'payment_date', 'payment_method', 'transaction_id', 'remarks']
    success_url = reverse_lazy('fee_payments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.request.GET.get('student')
        if student_id:
            context['form'].fields['student_fee'].queryset = StudentFee.objects.filter(
                student_id=student_id,
                status__in=['pending', 'partially_paid']
            ).select_related('student', 'fee_structure')
        else:
            context['form'].fields['student_fee'].queryset = StudentFee.objects.filter(
                status__in=['pending', 'partially_paid']
            ).select_related('student', 'fee_structure')
        return context

class FeePaymentUpdateView(UpdateView):
    model = FeePayment
    template_name = 'fee_payment_form.html'
    fields = ['student_fee', 'amount', 'payment_date', 'payment_method', 'transaction_id', 'remarks']
    success_url = reverse_lazy('fee_payments')

class FeePaymentDeleteView(DeleteView):
    model = FeePayment
    template_name = 'fee_payment_confirm_delete.html'
    success_url = reverse_lazy('fee_payments')

# Dashboard/Home view for fees
def fees_dashboard(request):
    # Overall statistics
    total_students = Student.objects.count()
    total_fees_assigned = StudentFee.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    total_fees_paid = StudentFee.objects.aggregate(total=Sum('paid_amount'))['total'] or 0
    total_fees_due = StudentFee.objects.aggregate(total=Sum('due_amount'))['total'] or 0

    # Recent payments
    recent_payments = FeePayment.objects.select_related('student_fee__student').order_by('-payment_date')[:10]

    # Overdue fees
    today_str = request.GET.get('today')
    try:
        overdue_cutoff = date.fromisoformat(today_str) if today_str else date.today()
    except ValueError:
        overdue_cutoff = date.today()

    overdue_fees = StudentFee.objects.filter(
        Q(status='pending') | Q(status='partially_paid'),
        fee_structure__due_date__lt=overdue_cutoff
    ).select_related('student', 'fee_structure')[:10]

    # Payment methods distribution
    payment_methods = FeePayment.objects.values('payment_method').annotate(
        total=Sum('amount')
    ).order_by('-total')

    context = {
        'total_students': total_students,
        'total_fees_assigned': total_fees_assigned,
        'total_fees_paid': total_fees_paid,
        'total_fees_due': total_fees_due,
        'recent_payments': recent_payments,
        'overdue_fees': overdue_fees,
        'payment_methods': payment_methods,
    }

    return render(request, 'fees_dashboard.html', context)
