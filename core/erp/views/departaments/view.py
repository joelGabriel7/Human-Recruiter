from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView

from core.erp.forms import DepartmentsForm
from core.erp.models import *


# Create your views here.

class DepartamentListView(ListView):
    model = Departments
    template_name = 'departaments/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Departments.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listados de Departamentos'
        context['create_url'] = reverse_lazy('erp:departaments_create')
        context['list_url'] = reverse_lazy('erp:departaments_list')
        context['entity'] = 'Departamentos'
        return context


class DepartamentCreateView(CreateView):
    model = Departments
    form_class = DepartmentsForm
    template_name = 'departaments/create.html'
    success_url = reverse_lazy('erp:departaments_list')

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


    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     form = DepartmentsForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(self.success_url)
    #     self.object = None
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = form
    #     return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crea un Departamento'
        context['create_url'] = reverse_lazy('erp:departaments_create')
        context['list_url'] = reverse_lazy('erp:departaments_list')
        context['entity'] = 'Departamentos'
        context['action'] = 'add'
        return context