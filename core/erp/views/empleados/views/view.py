import json
from decimal import Decimal
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from core.erp.forms import *
from core.erp.models import *
from core.erp.mixins import *
from django.core.paginator import Paginator


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
                search_value = request.POST.get('search[value]', '')


                employees = Employee.objects.annotate(
                    full_name=Concat('person__firstname', Value(' '), 'person__lastname')
                ).filter(
                    Q(id__icontains=search_value) |
                    Q(hiring_date__icontains=search_value) |
                    Q(codigo__icontains=search_value) |
                    Q(full_name__icontains=search_value) |  # Búsqueda por nombre completo usando el método get_full_name
                    Q(department__name__icontains=search_value) |
                    Q(position__name__icontains=search_value) |
                    Q(turn__name__icontains=search_value) |
                    Q(salary__icontains=search_value) |
                    Q(estado__icontains=search_value)
                ).order_by('id')

                e = Employee.objects.all().count()

                paginator = Paginator(employees, request.POST.get('length', e))
                start = int(request.POST.get('start', 0))
                length = int(request.POST.get('length', 10))
                page_number = start // length + 1
                page = paginator.get_page(page_number)

                data = {
                    'data': [
                        {
                            'id': employee.id,
                            'hiring_date': employee.hiring_date.strftime('%Y-%m-%d'),
                            'codigo': employee.codigo,
                            'full_name': employee.get_full_name(),
                            'department__name': employee.department.name,
                            'position__name': employee.position.name,
                            'turn__name': employee.turn.name,
                            'salary': float(employee.salary),
                            'estado': employee.estado,
                        }
                        for employee in page
                    ],
                    'recordsTotal': employees.count(),
                    'recordsFiltered': paginator.count,
                }
            elif action == 'deactive':
                employe = Employee.objects.get(pk=request.POST['id'])
                if employe.estado == 'Contratado' or employe.estado == 'Vacaciones':
                        employe.estado = 'Despedido'
                        employe.save()
                else:
                    employe.save()        
            elif action == 'active':
                employe = Employee.objects.get(pk=request.POST['id'])
                if employe.estado == 'Despedido':
                        employe.estado = 'Contratado' #Contratado
                        employe.save()
                else:
                    employe.save()  
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


class EmpleadoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
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


class EmpleadoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
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

