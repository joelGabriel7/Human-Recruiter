import json
from decimal import Decimal
from datetime import date
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from core.erp.models import Headings


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)


class DescuentosListView(TemplateView):
    template_name = 'descuentos/list.html'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Headings.objects.all().order_by('type', 'order'):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No se ha seleccionado ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        serialized_data = json.dumps(data, cls=CustomJSONEncoder)
        return HttpResponse(serialized_data, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(DescuentosListView, self).get_context_data()
        context['title'] = 'Listado de items de descuentos'
        context['entity'] = 'Items'
        return context
