
import json
from decimal import Decimal
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from core.erp.forms import *
from core.erp.models import *
from core.erp.mixins import *

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)
class SelectListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,TemplateView):
    model = Selection
    template_name = 'seleccionados/list.html'
    permission_required = 'view_selection'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                data = list(Selection.objects.values(
                    'id',
                    'person__firstname',
                    'person__phone',
                    'vacants__posicion__name',
                    'vacants__max_salary',
                    'vacants__min_salary',

                ))

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        serialized_data = json.dumps(data, cls=CustomJSONEncoder)
        return HttpResponse(serialized_data, content_type='application/json')


    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Lista de Aplicantes'
            context['entity'] = 'Aplicantes'
            context['list_url'] = reverse_lazy('erp:select_list')
            context['create_url'] = reverse_lazy('erp:select_create')
            context['form'] = SelectionForm()
            return context

class SelectCreateView(CreateView):
    model = Selection
    form_class = SelectionForm
    template_name = 'seleccionados/create.html'
    success_url = reverse_lazy('erp:select_list')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':

                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Elige a un seleccionado'
        context['entity'] = 'Seleccionados'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('erp:select_list')
        context['create_url'] = reverse_lazy('erp:select_create')
        return context


class SelectUpdateView(UpdateView):
    model = Selection
    form_class = SelectionForm
    template_name = 'seleccionados/create.html'
    success_url = reverse_lazy('erp:select_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                data = []
                form = self.get_form()
                data = form.save()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edita a un seleccionado'
        context['entity'] = 'Seleccionados'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('erp:select_list')
        context['create_url'] = reverse_lazy('erp:select_create')
        return context


class SelectDeleteView(DeleteView):
    model = Selection
    template_name = 'seleccionados/delete.html'

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
        context['title'] = 'Elimina a un seleccionado'
        context['entity'] = 'Seleccionado'
        context['list_url'] = reverse_lazy('erp:select_list')
        return context
