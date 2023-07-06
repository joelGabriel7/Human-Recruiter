import json
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView

from config import settings
from core.user.forms import UserForm, UserProfileForm

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


class UserChangeGroup(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user
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
        context['title'] = 'Edición de Perfil'
        context['entity'] = 'Perfil'
        context['action'] = 'edit'
        context['list_url'] = self.success_url

        return context


class UserChangePasswordView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        # Class
        form.fields['old_password'].widget.attrs['class']= 'form-control'
        form.fields['new_password1'].widget.attrs['class']= 'form-control'
        form.fields['new_password2'].widget.attrs['class']= 'form-control'
        form.fields['new_password2'].widget.attrs['autocomplete']= 'off'
        # placeholder
        form.fields['old_password'].widget.attrs['placeholder']= 'Ingrese su nueva contraseña '
        form.fields['new_password1'].widget.attrs['placeholder']= 'Ingrese su nueva contraseña '
        form.fields['new_password2'].widget.attrs['placeholder']= 'Repita su contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambiar Contraseña'
        context['entity'] = 'Password'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
