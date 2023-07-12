from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.erp.forms import *
from core.erp.models import *
from core.erp.mixins import *

class VacantsListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Vacants
    template_name = 'vacante/list.html'
    permission_required = 'view_vacants'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Vacants.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listados de Vacantes'
        context['create_url'] = reverse_lazy('erp:vacante_create')
        context['list_url'] = reverse_lazy('erp:vacante_list')
        context['entity'] = 'Vacantes'
        return context


class VacantsCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Vacants
    form_class = VacantsForm
    template_name = 'vacante/create.html'
    permission_required = 'add_vacants'

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
        context['title'] = 'Crea una Vacantes'
        context['entity'] = 'Vacantes'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('erp:vacante_list')
        context['create_url'] = reverse_lazy('erp:vacante_create')
        return context


class VacantsUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Vacants
    form_class = VacantsForm
    template_name = 'vacante/create.html'
    permission_required = 'change_vacants'

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

        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edita una Vacantes'
        context['entity'] = 'Vacantes'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('erp:vacante_list')
        context['create_url'] = reverse_lazy('erp:vacante_create')
        return context


class VacantsDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Vacants
    template_name = 'vacante/delete.html'
    permission_required = 'delete_vacants'
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
        context['title'] = 'Elimina una Vacante'
        context['entity'] = 'Vacantes'
        context['list_url'] = reverse_lazy('erp:vacante_list')
        context['create_url'] = reverse_lazy('erp:vacante_create')
        return context