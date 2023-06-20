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
                    queryset = queryset.filter(salary__year=year)
                if len(month):
                    queryset = queryset.filter(salary__month=month)
                if len(pks):
                    queryset = queryset.filter(employee_id__in=pks)
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_headings':
                data = []
                detail = SalaryDetail.objects.get(pk=request.POST['id'])
                for i in detail.salaryheadings_set.filter(headings__type='haberes', valor__gt=0).order_by(
                        'headings__order'):
                    data.append([i.headings.name, i.get_cant(), i.get_valor_format(), '---'])
                for i in detail.salaryheadings_set.filter(headings__type='descuentos', valor__gt=0).order_by(
                        'headings__order'):
                    data.append([i.headings.name, i.get_cant(), '---', i.get_valor_format()])
                data.append(['Subtotal de Ingresos', '---', '---', detail.get_income_format()])
                data.append(['Subtotal de Descuentos', '---', '---', detail.get_expenses_format()])
                data.append(['Total a recibir', '---', '---', detail.get_total_amount_format()])
            elif action == 'upload_excel':
                with transaction.atomic():
                    year = int(request.POST['year'])
                    month = int(request.POST['month'])
                    archive = request.FILES['archive']
                    workbook = load_workbook(archive, keep_vba=True, read_only=True, data_only=True, keep_links=True)
                    wb = workbook[workbook.sheetnames[0]]
                    columns = []
                    for cell in wb.iter_rows(min_row=1, max_row=1, min_col=7):
                        for row in cell:
                            columns.append(row.value)
                    max_column = wb.max_column - 1
                    for cell in wb.iter_rows(min_row=2, max_row=wb.max_row):
                        row = cell[0].row
                        employee = Employee.objects.get(code=wb.cell(row=row, column=1).value)
                        salary_detail = SalaryDetail()
                        queryset = SalaryDetail.objects.filter(employee=employee, salary__year=year,
                                                               salary__month=month)
                        if queryset.exists():
                            salary_detail = queryset[0]
                        else:
                            salary = Salary.objects.get_or_create(year=year, month=month)
                            salary_detail.salary = salary[0]
                            salary_detail.employee = employee
                            salary_detail.save()
                        index = 0
                        position = 7
                        salary_detail.salaryheadings_set.all().delete()
                        salary_detail.salaryheadings_set.all().delete()
                        while position < max_column:
                            code = columns[index]
                            if code in 'Subtotal':
                                position += 1
                                index += 1
                                continue
                            detail = SalaryHeadings()
                            detail.salary_detail_id = salary_detail.id
                            if code.__contains__('Cantidad.'):
                                code = code.split('.')[-1]
                                detail.headings = Headings.objects.get(code=code)
                                detail.cant = wb.cell(row=row, column=position).value
                                valor = str(wb.cell(row=row, column=position + 1).value)
                                detail.valor = valor.replace('.', '')
                                index += 2
                                position += 2
                            else:
                                detail.headings = Headings.objects.get(name=code)
                                valor = str(wb.cell(row=row, column=position).value)
                                detail.valor = valor.replace('.', '')
                                index += 1
                                position += 1
                            detail.save()
                        salary_detail.income = salary_detail.salaryheadings_set.filter(
                            headings__type='haberes').aggregate(
                            result=Coalesce(Sum('valor'), 0.00, output_field=FloatField())).get('result')
                        salary_detail.expenses = salary_detail.salaryheadings_set.filter(
                            headings__type='descuentos').aggregate(
                            result=Coalesce(Sum('valor'), 0.00, output_field=FloatField())).get('result')
                        salary_detail.total_amount = float(salary_detail.income) - float(salary_detail.expenses)
                        salary_detail.save()
            elif action == 'search_employee':
                data = []
                term = request.POST['term']
                for i in Employee.objects.filter(
                        Q(user__names__icontains=term) | Q(dni__icontains=term) | Q(code__icontains=term)).order_by(
                        'user__names')[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'remove_salaries':
                request.session['salaries'] = {}
                pks = json.loads(request.POST['pks'])
                request.session['salaries']['year'] = int(request.POST['year'])
                month = request.POST['month']
                request.session['salaries']['month'] = {}
                if len(month):
                    request.session['salaries']['month']['id'] = int(month)
                    request.session['salaries']['month']['name'] = MONTHS[int(month)][1]
                request.session['salaries']['employees'] = {}
                if len(pks):
                    request.session['salaries']['employees'] = Employee.objects.filter(id__in=pks)
                data['url'] = str(reverse_lazy('salary_delete'))
            elif action == 'export_salaries_excel':
                year = request.POST['year']
                month = request.POST['month']
                pks = json.loads(request.POST['pks'])
                queryset = SalaryDetail.objects.filter(salary__year=year)
                if len(month):
                    queryset = queryset.filter(salary__month=month)
                if len(pks):
                    queryset = queryset.filter(employee_id__in=pks)
                headers = {
                    'Código': 15,
                    'Empleado': 35,
                    'Sección': 35,
                    'Cargo': 35,
                    'Número de documento': 35,
                    'Fecha de ingreso': 35,
                }
                headings = Headings.objects.filter()
                for i in headings.filter(type='haberes').order_by('order'):
                    if i.has_quantity:
                        key = f'Cantidad {i.name}'
                        headers[key] = 45
                    headers[i.name] = 55
                headers['Subtotal'] = 50
                for i in headings.filter(type='descuentos').order_by('order'):
                    if i.has_quantity:
                        key = f'Cantidad {i.name}'
                        headers[key] = 45
                    headers[i.name] = 55
                headers['Total Descuento'] = 50
                headers['Total a Cobrar'] = 40
                output = BytesIO()
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet('planilla')
                cell_format = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})
                row_format = workbook.add_format({'align': 'center', 'border': 1})
                index = 0
                for name, width in headers.items():
                    worksheet.set_column(first_col=0, last_col=index, width=width)
                    worksheet.write(0, index, name, cell_format)
                    index += 1
                row = 1
                for salary_detail in queryset.order_by('employee'):
                    worksheet.write(row, 0, salary_detail.employee.code, row_format)
                    worksheet.write(row, 1, salary_detail.employee.user.names, row_format)
                    worksheet.write(row, 2, salary_detail.employee.area.name, row_format)
                    worksheet.write(row, 3, salary_detail.employee.position.name, row_format)
                    worksheet.write(row, 4, salary_detail.employee.dni, row_format)
                    worksheet.write(row, 5, salary_detail.employee.hiring_date_format(), row_format)
                    index = 5
                    for heading in headings.filter(type='haberes').order_by('order'):
                        salary_headings = salary_detail.salaryheadings_set.filter(headings_id=heading.id)
                        if salary_headings.exists():
                            salary_headings = salary_headings[0]
                            if heading.has_quantity:
                                worksheet.write(row, index + 1, salary_headings.get_cant(), row_format)
                                worksheet.write(row, index + 2, salary_headings.get_valor_format(), row_format)
                                index += 2
                            else:
                                worksheet.write(row, index + 1, salary_headings.get_valor_format(), row_format)
                                index += 1
                        else:
                            if heading.has_quantity:
                                worksheet.write(row, index + 1, '0', row_format)
                                worksheet.write(row, index + 2, '0.00', row_format)
                                index += 2
                            else:
                                worksheet.write(row, index + 1, '0.00', row_format)
                                index += 1
                    index += 1
                    worksheet.write(row, index, salary_detail.get_income_format(), row_format)
                    for heading in headings.filter(type='descuentos').order_by('order'):
                        salary_headings = salary_detail.salaryheadings_set.filter(headings_id=heading.id)
                        if salary_headings.exists():
                            salary_headings = salary_headings[0]
                            if heading.has_quantity:
                                worksheet.write(row, index + 1, salary_headings.get_cant(), row_format)
                                worksheet.write(row, index + 2, salary_headings.get_valor_format(), row_format)
                                index += 2
                            else:
                                worksheet.write(row, index + 1, salary_headings.get_valor_format(), row_format)
                                index += 1
                        else:
                            if heading.has_quantity:
                                worksheet.write(row, index + 1, '0', row_format)
                                worksheet.write(row, index + 2, '0.00', row_format)
                                index += 2
                            else:
                                worksheet.write(row, index + 1, '0.00', row_format)
                                index += 1
                    worksheet.write(row, index + 1, salary_detail.get_expenses_format(), row_format)
                    worksheet.write(row, index + 2, salary_detail.get_total_amount_format(), row_format)
                    row += 1
                workbook.close()
                output.seek(0)
                response = HttpResponse(output,
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response[
                    'Content-Disposition'] = f"attachment; filename='PLANILLA_{datetime.now().date().strftime('%d_%m_%Y')}.xlsx'"
                return response
            elif action == 'export_template':
                year = request.POST['year']
                month = request.POST['month']
                headers = {
                    'Código': 15,
                    'Empleado': 35,
                    'Sección': 35,
                    'Cargo': 35,
                    'Número de documento': 35,
                    'Fecha de ingreso': 35,
                }
                headings = Headings.objects.filter()
                for i in headings.filter(type='haberes').order_by('order'):
                    if i.has_quantity:
                        key = f'Cantidad.{i.code.lower()}'
                        headers[key] = 45
                    headers[i.name] = 55
                headers['Subtotal'] = 50
                for i in headings.filter(type='descuentos').order_by('order'):
                    if i.has_quantity:
                        key = f'Cantidad.{i.code.lower()}'
                        headers[key] = 45
                    headers[i.name] = 55
                headers['Total Descuento'] = 40
                headers['Total a Cobrar'] = 40
                output = BytesIO()
                workbook = xlsxwriter.Workbook(output)
                worksheet = workbook.add_worksheet('plantilla')
                cell_format = workbook.add_format({'bold': True, 'align': 'center', 'border': 1})
                row_format = workbook.add_format({'align': 'center', 'border': 1})
                index = 0
                for name, width in headers.items():
                    worksheet.set_column(first_col=0, last_col=index, width=width)
                    worksheet.write(0, index, name, cell_format)
                    index += 1
                row = 1
                for employee in Employee.objects.filter(user__is_active=True):
                    worksheet.write(row, 0, employee.code, row_format)
                    worksheet.write(row, 1, employee.user.names, row_format)
                    worksheet.write(row, 2, employee.area.name, row_format)
                    worksheet.write(row, 3, employee.position.name, row_format)
                    worksheet.write(row, 4, employee.dni, row_format)
                    worksheet.write(row, 5, employee.hiring_date_format(), row_format)
                    index = 5
                    salary_detail = SalaryDetail.objects.filter(employee=employee, salary__year=year,
                                                                salary__month=month)
                    for heading in headings.filter(type='haberes').order_by('order'):
                        salary_headings = SalaryHeadings.objects.filter(headings_id=heading.id,
                                                                        salary_detail__employee=employee,
                                                                        salary_detail__salary__year=year,
                                                                        salary_detail__salary__month=month)
                        if salary_headings.exists():
                            salary_headings = salary_headings[0]
                            if heading.has_quantity:
                                worksheet.write(row, index + 1, salary_headings.get_cant(), row_format)
                                worksheet.write(row, index + 2, salary_headings.get_valor_format(), row_format)
                                index += 2
                            else:
                                worksheet.write(row, index + 1, salary_headings.get_valor_format(), row_format)
                                index += 1
                        else:
                            if heading.has_quantity:
                                if heading.code == 'salario':
                                    worksheet.write(row, index + 1, employee.get_amount_of_assists(year, month),
                                                    row_format)
                                    worksheet.write(row, index + 2, float(employee.remuneration), row_format)
                                else:
                                    worksheet.write(row, index + 1, '0', row_format)
                                    worksheet.write(row, index + 2, '0.00', row_format)
                                index += 2
                            else:
                                worksheet.write(row, index + 1, '0.00', row_format)
                                index += 1
                    index += 1
                    if salary_detail.exists():
                        worksheet.write(row, index, salary_detail[0].get_income_format(), row_format)
                    else:
                        worksheet.write(row, index, '0.00', row_format)
                    for heading in headings.filter(type='descuentos').order_by('order'):
                        salary_headings = SalaryHeadings.objects.filter(headings_id=heading.id,
                                                                        salary_detail__employee=employee,
                                                                        salary_detail__salary__year=year,
                                                                        salary_detail__salary__month=month)
                        if salary_headings.exists():
                            salary_headings = salary_headings[0]
                            if heading.has_quantity:
                                worksheet.write(row, index + 1, salary_headings.get_cant(), row_format)
                                worksheet.write(row, index + 2, salary_headings.get_valor_format(), row_format)
                                index += 2
                            else:
                                worksheet.write(row, index + 1, salary_headings.get_valor_format(), row_format)
                                index += 1
                        else:
                            if heading.has_quantity:
                                worksheet.write(row, index + 1, '0', row_format)
                                worksheet.write(row, index + 2, '0.00', row_format)
                                index += 2
                            else:
                                worksheet.write(row, index + 1, '0.00', row_format)
                                index += 1
                    if salary_detail.exists():
                        worksheet.write(row, index + 1, salary_detail[0].get_expenses_format(), row_format)
                        worksheet.write(row, index + 2, salary_detail[0].get_total_amount_format(), row_format)
                    else:
                        worksheet.write(row, index + 1, '0.00', row_format)
                        worksheet.write(row, index + 2, '0.00', row_format)
                    row += 1
                workbook.close()
                output.seek(0)
                response = HttpResponse(output,
                                        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response[
                    'Content-Disposition'] = f"attachment; filename='PLANILLA_{datetime.now().date().strftime('%d_%m_%Y')}.xlsx'"
                return response
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super(SalaryListView, self).get_context_data()
        context['title'] = 'Listado de Nomina'
        context['entity'] = 'Nomina'
        return context