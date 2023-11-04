from config.wsgi import *
from django.template.loader import get_template
from weasyprint import HTML
from core.erp.models import *
import datetime
from django.http import HttpResponse


def report_vacations():
    vacations = Vacations.objects.all()
    company = Company.objects.first()
    current_day = datetime.date.today()
    template = get_template("pdf_vacations.html")
    context = {'fecha': current_day, "vacations": vacations, 'compañia': company}
    html_template = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Solicitud_de_Vacaciones.pdf"'
    HTML(string=html_template).write_pdf(response)
    return response
report_vacations()
