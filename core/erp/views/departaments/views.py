from django.shortcuts import render
from django.views.generic import ListView
from core.erp.models import *


# Create your views here.

class DepartamentListView(ListView):
    model = Departments
    template_name = 'departaments/list.html'
