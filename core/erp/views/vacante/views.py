from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
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

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)
class VacantsListView(LoginRequiredMixin,ValidatePermissionRequiredMixin,ListView):
    model = Vacants
    template_name = 'vacante/list.html'
    permission_required = 'view_vacants'
    paginate_by = 10

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                queryset = Vacants.objects.all().order_by('id')
                search_value = request.POST.get('search[value]', '')

                if search_value:
                    queryset = queryset.filter(
                        Q(posicion__name__contains=search_value) |
                        Q(description__contains=search_value) |
                        Q(min_salary__contains=search_value) |
                        Q(max_salary__contains=search_value)
                    ).order_by('id')

                paginator = Paginator(queryset, request.POST.get('length', 10))
                page_number = int(request.POST.get('start', 0)) // int(request.POST.get('length', 10)) + 1
                page = paginator.get_page(page_number)

                data = {
                    'data': [item.toJSON() for item in page],
                    'recordsTotal': queryset.count(),
                    'recordsFiltered': paginator.count,
                }

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        serialized_data = json.dumps(data, cls=CustomJSONEncoder)
        return HttpResponse(serialized_data, content_type='application/json')

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


