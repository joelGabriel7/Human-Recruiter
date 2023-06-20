import json
from datetime import datetime
from io import BytesIO
import xlsxwriter
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum, Q, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.base import View, TemplateView
from openpyxl import load_workbook
from decimal import Decimal
from datetime import date

from core.erp.choice import MONTHS
from core.erp.forms import SalaryForm
from core.erp.models import Salary, SalaryDetail, Employee, Headings, SalaryHeadings


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj)


class SalaryListView(FormView):
    form_class = SalaryForm
    template_name = 'salary/list.html'

    def get_form(self, form_class=None):
        form = SalaryForm()
        form.fields['year'].initial = datetime.now().date().year
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search':
                data = []
                year = request.POST['year']
                month = request.POST['month']
                pks = json.loads(request.POST['pks'])
                queryset = SalaryDetail.objects.filter()
                if len(year):
                    queryset = SalaryDetail.objects.filter(salary__year=year)
                if len(month):
                    queryset = SalaryDetail.objects.filter(salary__month=month)
                if len(pks):
                    queryset = SalaryDetail.objects.filter(employee__id__in=pks)
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_employee':
                data = []
                term = request.POST['term']
                for i in Employee.objects.filter(Q(person__firstname__icontains=term) | Q(person__cedula__icontains=term) | Q(codigo__icontains=term)).order_by('person__employee')[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            # elif action == 'search_detail_headings':
            #         data = []
            #         detail = SalaryDetail.objects.get(pk=request.POST['id'])
            #         for i in detail.salaryheadings_set.filter(headings__type='haberes', valor__gt=0).order_by(
            #                 'headings__order'):
            #             data.append([i.headings.name, i.get_cant(), i.get_valor_format(), '---'])
            #         for i in detail.salaryheadings_set.filter(headings__type='descuentos', valor__gt=0).order_by(
            #                 'headings__order'):
            #             data.append([i.headings.name, i.get_cant(), '---', i.get_valor_format()])
            #         data.append(['Subtotal de Ingresos', '---', '---', detail.get_income_format()])
            #         data.append(['Subtotal de Descuentos', '---', '---', detail.get_expenses_format()])
            #         data.append(['Total a recibir', '---', '---', detail.get_total_amount_format()])

            # elif action == 'export_salaries_excel':
            #     year = request.POST['year']
            #     month = request.POST['month']
            #     pks = json.loads(request.POST['pks'])
            #     queryset = SalaryDetail.objects.filter(salary__year=year)
            #     if len(month):
            #         queryset = queryset.filter(salary__month=month)
            #     if len(pks):
            #         queryset = queryset.filter(employee_id__in=pks)
            #     headers = {
            #         'Código': 15,
            #         'Empleado': 35,
            #         'Sección': 35,
            #         'Cargo': 35,
            #         'Número de documento': 35,
            #         'Fecha de ingreso': 35,
            #     }
            #     headings = Headings.objects.filter()
            #     for i in headings.filter(type='haberes').order_by('order'):
            #         if i.has_quantity:
            #             key = f'Cantidad {i.name}'
            #             headers[key] = 45
            #         headers[i.name] = 55
            #     headers['Subtotal'] = 50
            #     for i in headings.filter(type='descuentos').order_by('order'):
            #         if i.has_quantity:
            #             key = f'Cantidad {i.name}'
            #             headers[key] = 45
            #         headers[i.name] = 55
            #     headers['Total Descuento'] = 50
            #     headers['Total a Cobrar'] = 40
            #     output = BytesIO()
            #     workbook = xlsxwriter.Workbook(output)
            #     worksheet = workbook.add_worksheet('planilla')
            #     cell_format = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})
            #     row_format = workbook.add_format({'align': 'center', 'border': 1})
            #     index = 0
            #     for name, width in headers.items():
            #         worksheet.set_column(first_col=0, last_col=index, width=width)
            #         worksheet.write(0, index, name, cell_format)
            #         index += 1
            #     row = 1
            #     for salary_detail in queryset.order_by('employee'):
            #         worksheet.write(row, 0, salary_detail.employee.code, row_format)
            #         worksheet.write(row, 1, salary_detail.employee.user.names, row_format)
            #         worksheet.write(row, 2, salary_detail.employee.area.name, row_format)
            #         worksheet.write(row, 3, salary_detail.employee.position.name, row_format)
            #         worksheet.write(row, 4, salary_detail.employee.dni, row_format)
            #         worksheet.write(row, 5, salary_detail.employee.hiring_date_format(), row_format)
            #         index = 5
            #         for heading in headings.filter(type='haberes').order_by('order'):
            #             salary_headings = salary_detail.salaryheadings_set.filter(headings_id=heading.id)
            #             if salary_headings.exists():
            #                 salary_headings = salary_headings[0]
            #                 if heading.has_quantity:
            #                     worksheet.write(row, index + 1, salary_headings.get_cant(), row_format)
            #                     worksheet.write(row, index + 2, salary_headings.get_valor_format(), row_format)
            #                     index += 2
            #                 else:
            #                     worksheet.write(row, index + 1, salary_headings.get_valor_format(), row_format)
            #                     index += 1
            #             else:
            #                 if heading.has_quantity:
            #                     worksheet.write(row, index + 1, '0', row_format)
            #                     worksheet.write(row, index + 2, '0.00', row_format)
            #                     index += 2
            #                 else:
            #                     worksheet.write(row, index + 1, '0.00', row_format)
            #                     index += 1
            #         index += 1
            #         worksheet.write(row, index, salary_detail.get_income_format(), row_format)
            #         for heading in headings.filter(type='descuentos').order_by('order'):
            #             salary_headings = salary_detail.salaryheadings_set.filter(headings_id=heading.id)
            #             if salary_headings.exists():
            #                 salary_headings = salary_headings[0]
            #                 if heading.has_quantity:
            #                     worksheet.write(row, index + 1, salary_headings.get_cant(), row_format)
            #                     worksheet.write(row, index + 2, salary_headings.get_valor_format(), row_format)
            #                     index += 2
            #                 else:
            #                     worksheet.write(row, index + 1, salary_headings.get_valor_format(), row_format)
            #                     index += 1
            #             else:
            #                 if heading.has_quantity:
            #                     worksheet.write(row, index + 1, '0', row_format)
            #                     worksheet.write(row, index + 2, '0.00', row_format)
            #                     index += 2
            #                 else:
            #                     worksheet.write(row, index + 1, '0.00', row_format)
            #                     index += 1
            #         worksheet.write(row, index + 1, salary_detail.get_expenses_format(), row_format)
            #         worksheet.write(row, index + 2, salary_detail.get_total_amount_format(), row_format)
            #         row += 1
            #     workbook.close()
            #     output.seek(0)
            #     response = HttpResponse(output,
            #                             content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            #     response[
            #         'Content-Disposition'] = f"attachment; filename='PLANILLA_{datetime.now().date().strftime('%d_%m_%Y')}.xlsx'"
            #     return response
            # elif action == 'export_salaries_pdf':
            #     year = request.POST['year']
            #     month = request.POST['month']
            #     pks = json.loads(request.POST['pks'])
            #     queryset = SalaryDetail.objects.filter(salary__year=year)
            #     if len(month):
            #         queryset = queryset.filter(salary__month=month)
            #     if len(pks):
            #         queryset = queryset.filter(employee_id__in=pks)
            #     context = {
            #         'salaries': queryset,
            #         'company': Company.objects.first(),
            #         'prints': [1, 2],
            #         'date_joined': datetime.now().date()
            #     }
            #     pdf_file = printer.create_pdf(context=context, template_name='salary/format/format2.html')
            #     return HttpResponse(pdf_file, content_type='application/pdf')
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        serialized_data = json.dumps(data, cls=CustomJSONEncoder)
        return HttpResponse(serialized_data, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(SalaryListView, self).get_context_data()
        context['title'] = 'Listado de Nomina'
        context['entity'] = 'Nomina'
        return context
