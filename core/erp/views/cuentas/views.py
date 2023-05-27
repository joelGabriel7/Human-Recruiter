from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from core.erp.forms import *
from core.erp.models import *


class AccountsListView(TemplateView):
    model = AccountsBank
    template_name = 'cuentas/list.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in AccountsBank.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                data = []
                account = AccountsBank()
                account.number = request.POST['number']
                account.type = request.POST['type']
                account.bank = request.POST['bank']
                account.save()
            elif action == 'edit':
                data = []
                account = AccountsBank.objects.get(pk=request.POST['id'])
                account.number = request.POST['number']
                account.type = request.POST['type']
                account.bank = request.POST['bank']
                account.save()
            elif action == 'delete':
                data = []
                account = AccountsBank.objects.get(pk=request.POST['id'])
                account.delete()

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de cuentas'
        context['entity'] = 'Cuentas'
        context['list_url'] = reverse_lazy('erp:cuenta_list')
        context['form'] = AccountsForm()
        return context
