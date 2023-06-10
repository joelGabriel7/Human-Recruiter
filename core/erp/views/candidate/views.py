from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.erp.forms import CandidateForm
from core.erp.models import *


# Create your views here.

class CandidateListView(ListView):
    model = Candidatos
    template_name = 'candidatos/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Candidatos.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listados de Candidatos'
        context['create_url'] = reverse_lazy('erp:candidatos_create')
        context['list_url'] = reverse_lazy('erp:candidatos_list')
        context['entity'] = 'Candidatos'
        return context


class CandidateCreateView(CreateView):
    model = Candidatos
    form_class = CandidateForm
    template_name = 'candidatos/create.html'
    success_url = reverse_lazy('erp:candidatos_list')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un candidato'
        context['entity'] = 'Candidatos'
        context['list_url'] = reverse_lazy('erp:candidatos_list')
        context['action'] = 'add'
        context['create_url'] = reverse_lazy('erp:candidatos_create')
        return context


class CandidateUpdateView(UpdateView):
    model = Candidatos
    form_class = CandidateForm
    template_name = 'candidatos/create.html'
    success_url = reverse_lazy('erp:candidatos_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de un candidato'
        context['entity'] = 'Candidatos'
        context['list_url'] = reverse_lazy('erp:candidatos_list')
        context['action'] = 'edit'
        context['create_url'] = reverse_lazy('erp:candidatos_create')
        return context


class CandidateDeleteView(DeleteView):
    model = Candidatos
    form_class = CandidateForm
    template_name = 'candidatos/delete.html'
    success_url = reverse_lazy('erp:candidatos_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de  un candidato'
        context['entity'] = 'Candidatos'
        context['list_url'] = reverse_lazy('erp:candidatos_list')
        context['create_url'] = reverse_lazy('erp:candidatos_create')
        return context
