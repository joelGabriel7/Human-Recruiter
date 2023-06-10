import json
from decimal import Decimal
from datetime import date
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import *
from core.erp.forms import *
from core.erp.models import *


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)


class AttendanceListView(FormView):
    form_class = AttendanceForm
    template_name = 'attendance/list.html'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Attendance.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date__range=[start_date, end_date])
                for i in queryset.order_by('employee__attendance__date'):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
            print(f'ERROR: {data}')
        serialized_data = json.dumps(data, cls=CustomJSONEncoder)
        return HttpResponse(serialized_data, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Asistencias'
        context['create_url'] = reverse_lazy('erp:asistencia_create')
        return context


class AttendanceCreateView(CreateView):
    model = Attendance
    template_name = 'attendance/create.html'
    form_class = AttendanceForm
    success_url = reverse_lazy('erp:asistencia_list')

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        print(request.POST['date'])
        try:
            if action == 'add':
                with transaction.atomic():
                    for i in json.loads(request.POST['attendance']):
                        date_time = datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d')
                        attendance = Attendance()
                        attendance.date = date_time
                        attendance.employee_id = i(i['id'])
                        attendance.observation = i['observation']
                        attendance.attendance = i['attendance']
                        attendance.save()
            elif action == 'generate_assistance':
                data=[]
                for i in Employee.objects.filter(person__isnull=False):
                    # print(i)
                    item = i.toJSON()
                    item['attendance'] = 0
                    item['observation'] = ''
                    data.append(item)
                    print(data)
            elif action == 'validate_data':
                data = {
                    'valid': not Attendance.objects.filter(date=request.POST['date'].strip()).exists()}
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        serialized_data = json.dumps(data, cls=CustomJSONEncoder)
        return HttpResponse(serialized_data, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuevo Registro de asistencia'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
