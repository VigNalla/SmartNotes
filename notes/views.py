from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NotesForm
from .models import Notes

class NotesDeleteView(LoginRequiredMixin,DeleteView):
    model = Notes
    success_url = reverse_lazy("notes.list")
    template_name = "notes/notes_delete.html"
    login_url = "/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note'] = self.get_object()
        return context

class NotesUpdateView(LoginRequiredMixin,UpdateView):
    model = Notes
    success_url = "/smart/notes"
    form_class = NotesForm
    login_url = "/login"

class NotesCreateView(LoginRequiredMixin,CreateView):
    model = Notes
    success_url = "/smart/notes"
    form_class = NotesForm
    login_url = "/login"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_list.html"
    login_url = "/login"

    def get_queryset(self):
        return self.request.user.notes.all()

class NotesDetailView(LoginRequiredMixin,DetailView):
    model = Notes
    context_object_name = "note"
    template_name = "notes/notes_detail.html"
    login_url = "/login"