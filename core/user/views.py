from typing import Any, Dict
from django.views.generic import ListView
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# Create your views here.

class UserListView(LoginRequiredMixin,ListView):
    model= User
    template_name= 'user/list.html'

    #@method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # def post(self,request):
    #     data = {}
    #     try:
    #         action = request.POST['action']
    #         if action == 'searchdata':
    #             data = []
    #             for i in User.objects.all():
    #                 data.append(i.toJson())
    #         else:
    #             data['error'] = 'Ha ocurrido un error'
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'Listado de usuarios'
        context['entity'] = 'Usuario'
        return context