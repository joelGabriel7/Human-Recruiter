from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.erp.forms import *
from core.erp.models import *
from core.erp.mixins import *
import json
from decimal import Decimal
from datetime import date
from django.utils import timezone

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)

class VacationsListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Vacations
    template_name = 'vacations/list.html'
    permission_required = 'view_vacations'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print('Funciona')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Vacations.objects.all():
                    data.append(i.toJSON())
            elif action == 'delete':
              vacations = Vacations.objects.get(pk=request.POST['id'])
              vacations.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        serialized_data = json.dumps(data, cls=CustomJSONEncoder)
        return HttpResponse(serialized_data, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listados de Vacaciones'
        context['entity'] = 'Vacaciones'
        context['create_url'] = reverse_lazy('erp:vacations_create')
        return context

class VacationsCreatView(LoginRequiredMixin,ValidatePermissionRequiredMixin, CreateView):
    model = Vacations
    form_class = VacationsForm
    template_name = 'Vacations/create.html'
    permission_required = 'add_vacations'

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
                data['error']= 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Solicitud de Vacaciones'
        context['entity'] = 'Vacaciones'
        context['list_url'] = reverse_lazy('erp:vacations_list')
        context['action'] = 'add'
        return context

class VacationsUpdateView(LoginRequiredMixin,ValidatePermissionRequiredMixin, UpdateView):
    model = Vacations
    form_class = VacationsForm
    template_name = 'Vacations/create.html'
    permission_required = 'change_vacations'

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
                data['error']= 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una solicitud de Vacaciones'
        context['entity'] = 'Vacaciones'
        context['list_url'] = reverse_lazy('erp:vacations_list')
        context['action'] = 'edit'
        return context

def finalizar_tareas_de_vacaciones():
    today = timezone.now().date()  # Obtiene la fecha actual sin la hora.
    # Filtra las vacaciones pendientes o aceptadas que han terminado.
    vacaciones_pendientes = Vacations.objects.filter(
        state_vacations__in=['Pendiente', 'Acceptada'],
        end_date__lte=today
    )

    for vacacion in vacaciones_pendientes:
        # Actualiza el estado de las vacaciones a 'Finalizada'.
        vacacion.state_vacations = 'Finalizada'
        vacacion.save()

        # Aquí puedes agregar el código para enviar un correo electrónico al empleado si lo deseas.
        # Por ejemplo, utilizando Django's EmailMessage.

        # También puedes realizar otras acciones que desees al finalizar las vacaciones.

    return f'Se han finalizado {len(vacaciones_pendientes)} tareas de vacaciones.'