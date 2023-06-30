from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from core.erp.forms import *
from core.erp.models import *


class SelectListView(LoginRequiredMixin,TemplateView):
    model = Selection
    template_name = 'seleccionados/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Selection.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                apply = Selection()
                apply.person = Candidatos.objects.get(pk=request.POST['person'])
                apply.vacants = Vacants.objects.get(pk=request.POST['vacants'])
                apply.save()
            elif action == 'edit':
                apply = Selection.objects.get(pk=request.POST['id'])
                apply.person = Candidatos.objects.get(pk=request.POST['person'])
                apply.vacants = Vacants.objects.get(pk=request.POST['vacants'])
                apply.save()
            elif action == 'delete':
                apply = Selection.objects.get(pk=request.POST['id'])
                apply.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Aplicantes'
        context['entity'] = 'Aplicantes'
        context['list_url'] = reverse_lazy('erp:select_list')
        context['form'] = SelectionForm()
        return context

# class SelectCreateView(CreateView):
#     model = Selection
#     form_class = SelectionForm
#     template_name = 'seleccionados/create.html'
#     success_url = reverse_lazy('erp:select_list')
#
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'add':
#                 data = []
#                 form = self.get_form()
#                 data = form.save()
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Elige a un seleccionado'
#         context['entity'] = 'Seleccionados'
#         context['action'] = 'add'
#         context['list_url'] = reverse_lazy('erp:select_list')
#         context['create_url'] = reverse_lazy('erp:select_create')
#         return context
#
#
# class SelectUpdateView(UpdateView):
#     model = Selection
#     form_class = SelectionForm
#     template_name = 'seleccionados/create.html'
#     success_url = reverse_lazy('erp:select_list')
#
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'edit':
#                 data = []
#                 form = self.get_form()
#                 data = form.save()
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Edita a un seleccionado'
#         context['entity'] = 'Seleccionados'
#         context['action'] = 'edit'
#         context['list_url'] = reverse_lazy('erp:select_list')
#         context['create_url'] = reverse_lazy('erp:select_create')
#         return context
#
#
# class SelectDeleteView(DeleteView):
#     model = Selection
#     template_name = 'seleccionados/delete.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             self.object.delete()
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Elimina a un seleccionado'
#         context['entity'] = 'Seleccionado'
#         context['list_url'] = reverse_lazy('erp:select_list')
#         return context
