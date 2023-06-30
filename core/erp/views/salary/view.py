import json
from datetime import datetime
from io import BytesIO
import xlsxwriter
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum, Q, FloatField, DecimalField
from django.db.models.functions import Coalesce, Cast
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.base import View, TemplateView
from openpyxl import load_workbook
from decimal import Decimal
from datetime import date
import openpyxl
from openpyxl.styles import Alignment, Border, Side
from openpyxl.utils import get_column_letter
# from openpyxl.writer.excel import save_virtual_workbook
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


class SalaryListView(LoginRequiredMixin,FormView):
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
                for i in Employee.objects.filter(
                        Q(person__firstname__icontains=term) | Q(person__cedula__icontains=term) | Q(
                            codigo__icontains=term)).order_by('person__employee')[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'search_detail_headings':
                data = []
                detail = SalaryDetail.objects.get(pk=request.POST['id'])
                for i in detail.salaryheadings_set.filter(headings__type='remuneracion', valor__gt=0).order_by(
                        'headings__order'):
                    data.append([i.headings.name, i.get_cant(), i.get_valor_format(), '---'])
                for i in detail.salaryheadings_set.filter(headings__type='descuentos', valor__gt=0).order_by(
                        'headings__order'):
                    data.append([i.headings.name, i.get_cant(), '---', i.get_valor_format()])
                data.append(['Subtotal de Ingresos', '---', '---', detail.get_income_format()])
                data.append(['Subtotal de Descuentos', '---', '---', detail.get_expenses_format()])
                data.append(['Total a recibir', '---', '---', detail.get_total_amount_format()])
            elif action == 'export_salaries_excel':
                year = request.POST['year']
                month = request.POST['month']
                pks = json.loads(request.POST['pks'])
                print(pks)
                queryset = SalaryDetail.objects.filter(salary__year=year)
                if len(month):
                    queryset = queryset.filter(salary__month=month)
                if len(pks):
                    queryset = queryset.filter(employee_id__in=pks)
                headers = {
                    'Empleados': 29.09,
                    'Cedula': 18,
                    'Cuenta': 18,
                    'Fecha de pago': 18,
                    'Total a recibir': 18,
                }

                workbook = openpyxl.Workbook()
                worksheet = workbook.active

                table_border = Border(left=Side(border_style='thin'), right=Side(border_style='thin'),
                                      top=Side(border_style='thin'), bottom=Side(border_style='thin'))

                header_font = openpyxl.styles.Font(bold=True)
                header_alignment = Alignment(horizontal='center')
                table_alignment = Alignment(horizontal='center', vertical='center')
                index = 1
                for col_num, (header, width) in enumerate(headers.items(), start=1):
                    column_letter = get_column_letter(col_num)
                    column_width = width  # Ajuste de ancho para el tamaño de la fuente

                    worksheet.column_dimensions[column_letter].width = column_width
                    worksheet.cell(row=index, column=col_num, value=header).font = header_font
                    worksheet.cell(row=index, column=col_num).alignment = header_alignment
                for salary_detail in queryset.order_by('employee'):
                    index += 1
                    worksheet.cell(row=index, column=1, value=salary_detail.employee.get_full_name()).alignment = table_alignment
                    worksheet.cell(row=index, column=2, value=salary_detail.employee.person.cedula).alignment = table_alignment
                    worksheet.cell(row=index, column=3, value=salary_detail.employee.accounts.number).alignment = table_alignment
                    worksheet.cell(row=index, column=4, value=f" {salary_detail.salary.payment_date}").alignment = table_alignment
                    worksheet.cell(row=index, column=5,value=salary_detail.get_total_amount_format()).alignment = table_alignment
                # Aplicar bordes a todas las celdas de la tabla
                for row in worksheet.iter_rows(min_row=1, max_row=index, min_col=1, max_col=len(headers)):
                    for cell in row:
                        cell.border = table_border

                table_height = 30  # Altura deseada en puntos
                table_rows = index - 1  # Restar 1 para excluir la fila de encabezado
                table_top_margin = (table_height - table_rows * 7) // 2  # Calcular el margen superior para centrar la tabla

                for i in range(2, index + 1):
                    worksheet.row_dimensions[i].height = 15  # Altura de fila predeterminada
                    worksheet.row_dimensions[i].height += table_top_margin

                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response[
                    'Content-Disposition'] = f"attachment; filename='PLANILLA_{datetime.now().date().strftime('%d_%m_%Y')}.xlsx'"
                workbook.save(response)

                return response
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
        context['create_url'] = reverse_lazy('erp:salary_create')
        return context


class SalaryCreateView(LoginRequiredMixin,CreateView):
    model = Salary
    template_name = 'salary/create.html'
    form_class = SalaryForm
    success_url = reverse_lazy('erp:salary_list')

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    salary = \
                    Salary.objects.get_or_create(year=int(request.POST['year']), month=int(request.POST['month']))[0]
                    for i in json.loads(request.POST['headings']):
                        heading = i
                        employee = Employee.objects.get(pk=int(heading['employee']['id']))
                        salary_detail = SalaryDetail()
                        queryset = salary.salarydetail_set.filter(employee=employee)
                        if queryset.exists():
                            salary_detail = queryset[0]
                            salary_detail.salaryheadings_set.all().delete()
                        else:
                            salary_detail.salary_id = salary.id
                            salary_detail.employee_id = employee.id
                            salary_detail.save()
                        del heading['employee']
                        del heading['total_discounts']
                        del heading['total_charge']
                        del heading['total_assets']
                        for key, value in heading.items():
                            detail = SalaryHeadings()
                            detail.salary_detail_id = salary_detail.id
                            detail.headings_id = int(value['id'])
                            detail.cant = int(value['cant'])
                            detail.valor = int(value['amount'])
                            detail.save()
                        salary_detail.income = salary_detail.salaryheadings_set.filter(
                            headings__type='remuneracion').aggregate(
                            result=Coalesce(Sum('valor', ), 0.00, output_field=DecimalField())).get('result')
                        salary_detail.expenses = salary_detail.salaryheadings_set.filter(
                            headings__type='descuentos').aggregate(
                            result=Coalesce(Sum('valor', default=0.00), 0.00, output_field=DecimalField())).get(
                            'result')
                        salary_detail.total_amount = float(salary_detail.income) - float(salary_detail.expenses)
                        salary_detail.save()
            elif action == 'search_employee':
                data = []
                term = request.POST['term']
                for i in Employee.objects.filter(
                        Q(person__firstname__icontains=term) | Q(person__cedula__icontains=term) | Q(
                                codigo__icontains=term)).order_by('person__employee')[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'search_employees':
                detail = []
                year = int(request.POST['year'])
                month = int(request.POST['month'])
                employees_ids = json.loads(request.POST['employees_ids'])
                employees = Employee.objects.filter(person__isnull=False)
                if len(employees_ids):
                    employees = employees.filter(id_in=employees_ids)
                columns = [{'data': 'employees.person.first_name'}]
                headings = Headings.objects.filter(state=True)
                for i in headings.filter(type='remuneracion').order_by('type', 'order', 'has_quantity'):
                    if i.has_quantity:
                        columns.append({'data': f'{i.code}.cant'})
                    columns.append({'data': i.code})
                columns.append({'data': 'total_assets'})
                for i in headings.filter(type='descuentos').order_by('type', 'order'):
                    if i.has_quantity:
                        columns.append({'data': f'{i.code}.cant'})
                    columns.append({'data': i.code})
                columns.append({'data': 'total_assets'})
                columns.append({'data': 'total_charge'})
                for employee in employees:
                    heading = {}
                    for d in headings.filter(type='remuneracion').order_by('order'):
                        item = d.toJSON()
                        item['cant'] = 0
                        item['amount'] = 0.00
                        if d.code == 'salario':
                            item['amount'] = float(employee.salary)
                            item['cant'] = employee.get_amount_of_assists(year, month)
                        queryset = d.get_amount_detail_salary(employee=employee.id, year=year, month=month)
                        if queryset is not None:
                            item['amount'] = float(queryset.valor)
                            item['cant'] = queryset.cant
                        heading[d.code] = item
                    for d in headings.filter(type='descuentos').order_by('order'):
                        item = d.toJSON()
                        item['cant'] = 0
                        item['amount'] = 0.00
                        queryset = d.get_amount_detail_salary(employee=employee.id, year=year, month=month)
                        if queryset is not None:
                            item['amount'] = float(queryset.valor)
                            item['cant'] = queryset.cant
                        heading[d.code] = item
                    salary_detail = SalaryDetail.objects.filter(employee_id=employee.id, salary__year=year,
                                                                salary__month=month)
                    if salary_detail.exists():
                        salary_detail = salary_detail[0]
                        heading['total_assets'] = {'code': 'total_assets', 'amount': float(salary_detail.income)}
                        heading['total_discounts'] = {'code': 'total_discounts',
                                                      'amount': float(salary_detail.expenses)}
                        heading['total_charge'] = {'code': 'total_charge', 'amount': float(salary_detail.total_amount)}
                    else:
                        heading['total_assets'] = {'code': 'total_assets', 'amount': 0.00}
                        heading['total_discounts'] = {'code': 'total_discounts', 'amount': 0.00}
                        heading['total_charge'] = {'code': 'total_charge', 'amount': float(employee.salary)}
                    heading['employee'] = employee.toJSON()
                    detail.append(heading)
                data = {'detail': detail, 'columns': columns}
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        serialized_data = json.dumps(data, cls=CustomJSONEncoder)
        return HttpResponse(serialized_data, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Generar nueva nomina'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['assets'] = Headings.objects.filter(state=True, type='remuneracion').order_by('id')
        context['discounts'] = Headings.objects.filter(state=True, type='descuentos').order_by('id')
        return context
