import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.erp.models import *


# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['salaries'] = SalaryDetail.objects.filter().order_by('id')[0:10]
        context['year'] = datetime.datetime.now().year
        context['month'] = MONTHS[datetime.datetime.now().month][1]
        context['employee'] = Employee.objects.filter().order_by('-id')[0:10]
        context['positions'] = EmployeePositions.objects.all().count()
        context['areas'] = Departments.objects.all().count()
        context['headings'] = Headings.objects.all().count()
        context['employees'] = Employee.objects.all().count()
        return context
