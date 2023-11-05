from config.wsgi import *
from django.template.loader import get_template
from weasyprint import HTML
from core.erp.models import *
import datetime
from django.http import HttpResponse


def report():
    empleados = Employee.objects.filter()
    company = Company.objects.first()
    current_day = datetime.date.today()
    template = get_template("pdf_report_employee.html")
    context = {
        'empleados': empleados,
        'company': company,
        'fecha': current_day,

    }
    html_template = template.render(context)
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="Reporte Personal.pdf"'
    HTML(string=html_template).write_pdf('Reporte Personal.pdf')
    # return response


report()
