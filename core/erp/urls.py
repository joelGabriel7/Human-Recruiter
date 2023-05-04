from django.urls import path
from core.erp.views.departaments.view import *

app_name = 'erp'

urlpatterns = [

    path('departaments/list/', DepartamentListView.as_view(), name='departaments_list'),
    path('departaments/create/', DepartamentCreateView.as_view(), name='departaments_create'),

]