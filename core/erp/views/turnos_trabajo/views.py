from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from core.erp.models import *
from core.erp.forms import *


class TurnJobListView(ListView):
    model = EmployeeTurn
    template_name = 'turnos_trabajo/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in EmployeeTurn.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Turnos'
        context['create_url'] = reverse_lazy('erp:turno_trabajo_create')
        context['list_url'] = reverse_lazy('erp:turno_trabajo_list')
        context['entity']= 'Horarios'
        return context

class TurnJobCreateView(CreateView):
    model = EmployeeTurn
    form_class = EmployeeTurnForm
    template_name = 'turnos_trabajo/create.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pass


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de un turno'
        context['entity'] = 'Horarios'
        context['list_url'] = reverse_lazy('erp:turno_trabajo_list')
        return context
