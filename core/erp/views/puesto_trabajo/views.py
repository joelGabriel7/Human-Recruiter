from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from core.erp.models import *
from core.erp.forms import *


class PositionsJobListView(ListView):
    model = EmployeePositions
    template_name = 'positions/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in EmployeePositions.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Posiciones'
        context['entity'] = 'Posiciones'
        context['create_url'] = reverse_lazy('erp:position_create')
        context['list_url'] = reverse_lazy('erp:position_list')
        return context


class PositionsJobCreateView(CreateView):
    model = EmployeePositions
    form_class = PositionsForm
    template_name = 'positions/create.html'
    success_url = reverse_lazy('erp:position_list')

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
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crea una Posicion'
        context['list_url'] = self.success_url
        context['entity'] = 'Posicion'
        context['action'] = 'add'
        return context


class PositionsJobUpdateView(UpdateView):
    model = EmployeePositions
    form_class = PositionsForm
    template_name = 'positions/create.html'
    success_url = reverse_lazy('erp:position_list')

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
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edita una Posicion'
        context['list_url'] = self.success_url
        context['entity'] = 'Posicion'
        context['action'] = 'edit'
        return context


class PositionsJobDeleteView(DeleteView):
    model = EmployeePositions
    template_name = 'positions/delete.html'
    success_url = reverse_lazy('erp:position_list')

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
        context['title'] = 'Eliminación de una Posicion'
        context['entity'] = 'Posiciones'
        context['list_url'] = self.success_url
        return context
