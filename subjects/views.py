from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Subject

class SubjectListView(ListView):
    model = Subject
    template_name = 'subjects.html'
    context_object_name = 'subjects'

class SubjectDetailView(DetailView):
    model = Subject
    template_name = 'subject_detail.html'

class SubjectCreateView(CreateView):
    model = Subject
    template_name = 'subject_form.html'
    fields = ['name', 'teacher', 'description']
    success_url = reverse_lazy('subjects')

class SubjectUpdateView(UpdateView):
    model = Subject
    template_name = 'subject_form.html'
    fields = ['name', 'teacher', 'description']
    success_url = reverse_lazy('subjects')

class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'subject_confirm_delete.html'
    success_url = reverse_lazy('subjects')
