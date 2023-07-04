from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.user.forms import UserForm
from core.erp.models import *
from core.user.models import User


# Create your views here.

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in User.objects.all():
                    item= i.toJson()
                    data.append(item)

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listados de Usuarios'
        context['create_url'] = reverse_lazy('user:user_create')
        context['list_url'] = reverse_lazy('user:user_list')
        context['entity'] = 'Usuarios'
        return context


class UserCreateView(LoginRequiredMixin,CreateView):
    model = User
    form_class = UserForm 
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, **kwargs):
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
        context['title'] = 'Crea una Usuario'
        context['entity'] = 'Usuarios'
        context['action'] = 'add'
        context['list_url'] = self.success_url
      
        return context
    
class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UserForm 
    template_name = 'user/create.html'
    success_url = reverse_lazy('user:user_list')
    

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
        context['title'] = 'Edición de un Usuario'
        context['entity'] = 'Usuarios'
        context['action'] = 'edit'
        context['list_url'] = self.success_url
      
        return context
        
class UserDeleteView(LoginRequiredMixin,DeleteView):
    model = User
    template_name = 'delete.html'
    success_url = reverse_lazy('user:user_list')

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
        context['title'] = 'Eliminación de un usuario'
        context['entity'] = 'Usuarios'
        context['list_url'] = self.success_url
        return context
