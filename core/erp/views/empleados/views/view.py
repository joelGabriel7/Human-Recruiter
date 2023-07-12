import json
from decimal import Decimal
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class EmpleadoListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Employee
    template_name = 'empleado/list.html'
    permission_required = 'view_employee'
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = list(Employee.objects.values(
                    'id',
                    'hiring_date',
                    'codigo',
                    'person__firstname',
                    'department__name',
                    'position__name',
                    'turn__name',
                    'salary',
                    'estado',

                ))
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        serialized_data = json.dumps(data, cls=CustomJSONEncoder)
        return HttpResponse(serialized_data, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de empleados'
        context['entity'] = 'Empleados'
        context['list_url'] = reverse_lazy('erp:empleados_list')
        context['create_url'] = reverse_lazy('erp:empleados_create')
        return context


class EmpleadoCreateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,CreateView):
    model = Employee
    template_name = 'empleado/create.html'
    form_class = EmployeForm
    permission_required = 'add_employee'

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
        context['title'] = 'Crea un empleado'
        context['entity'] = 'Empleados'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('erp:empleados_list')
        context['create_url'] = reverse_lazy('erp:empleados_create')
        return context


class EmpleadoUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin,UpdateView):
    model = Employee
    template_name = 'empleado/create.html'
    form_class = EmployeForm
    permission_required = 'change_employee'

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
        context['title'] = 'Edita un empleado'
        context['entity'] = 'Empleados'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('erp:empleados_list')
        context['create_url'] = reverse_lazy('erp:empleados_create')
        return context


class EmpleadoDeleteView(LoginRequiredMixin,ValidatePermissionRequiredMixin,DeleteView):
    model = Employee
    template_name = 'empleado/delete.html'
    success_url = reverse_lazy('erp:empleados_list')
    permission_required = 'delete_employee'

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
        context['title'] = 'Elimina un empleado'
        context['entity'] = 'Empleados'
        context['list_url'] = self.success_url
        return context
