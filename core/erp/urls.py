from django.urls import path

from core.erp.views.candidate.views import *
from core.erp.views.company.views import CompanyUpdateView

from core.erp.views.departaments.view import *
from core.erp.views.empleados.views.view import *
from core.erp.views.puesto_trabajo.views import *
from core.erp.views.salary.view import *
from core.erp.views.seleccionados.views import *
from core.erp.views.turnos_trabajo.views import *
from core.erp.views.vacante.views import *
from core.erp.views.asistencia.views import *
from core.erp.views.descuentos.view import *
from core.erp.views.Vacations.views import *

app_name = 'erp'

urlpatterns = [
    # Departamentos
    path('departaments/list/', DepartamentListView.as_view(), name='departaments_list'),
    # path('departaments/create/', DepartamentCreateView.as_view(), name='departaments_create'),
    # path('departaments/edit/<int:pk>/', DepartamentUpdateView.as_view(), name='departaments_edit'),
    # path('departaments/delete/<int:pk>/', DepartamentDeleteView.as_view(), name='departaments_delete'),

    # Puesto_trabajo
    path('puesto/list/', PositionsJobListView.as_view(), name='position_list'),
    path('puesto/add/', PositionsJobCreateView.as_view(), name='position_create'),
    path('puesto/update/<int:pk>/', PositionsJobUpdateView.as_view(), name='position_update'),
    path('puesto/delete/<int:pk>/', PositionsJobDeleteView.as_view(), name='position_delete'),

    # Turno trabajo
    path('turno_trabajo/list/', TurnJobListView.as_view(), name='turno_trabajo_list'),
    path('turno_trabajo/add/', TurnJobCreateView.as_view(), name='turno_trabajo_create'),
    path('turno_trabajo/edit/<int:pk>/', TurnJobUpdateView.as_view(), name='turno_trabajo_update'),
    path('turno_trabajo/delete/<int:pk>/', TurnJobDeleteView.as_view(), name='turno_trabajo_delete'),

    # Candidatos
    path('candidato/list/', CandidateListView.as_view(), name='candidatos_list'),
    path('candidato/add/', CandidateCreateView.as_view(), name='candidatos_create'),
    path('candidato/edit/<int:pk>/', CandidateUpdateView.as_view(), name='candidatos_update'),
    path('candidato/delete/<int:pk>/', CandidateDeleteView.as_view(), name='candidatos_delete'),

    # Vacantes
    path('vacante/list/', VacantsListView.as_view(), name='vacante_list'),
    path('vacante/add/', VacantsCreateView.as_view(), name='vacante_create'),
    path('vacante/edit/<int:pk>/', VacantsUpdateView.as_view(), name='vacante_update'),
    path('vacante/delete/<int:pk>/', VacantsDeleteView.as_view(), name='vacante_delete'),

    # Seleccionados

    path('select/list/', SelectListView.as_view(), name='select_list'),
    path('select/add/', SelectCreateView.as_view(), name='select_create'),
    path('select/edit/<int:pk>/', SelectUpdateView.as_view(), name='select_update'),
    path('select/delete/<int:pk>/', SelectDeleteView.as_view(), name='select_delete'),

    # Empleados
    path('empleados/list/', EmpleadoListView.as_view(), name='empleados_list'),
    path('empleados/add/', EmpleadoCreateView.as_view(), name='empleados_create'),
    path('empleados/edit/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleados_update'),
    path('empleados/delete/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleados_delete'),

    # Asistencia
    path('asistencia/list/', AssistanceListView.as_view(), name='asistencia_list'),
    path('asistencia/add/', AssistanceCreateView.as_view(), name='asistencia_create'),
    path('asistencia/update/<str:date_joined>/', AssistanceUpdateView.as_view(), name='asistencia_update'),
    path('asistencia/delete/<str:start_date>/<str:end_date>/', AssistanceDeleteView.as_view(), name='asistencia_delete'),

    # Conceptos de Descuentos
    path('descuento/list/', DescuentosListView.as_view(), name='descuento_list'),
    path('descuento/add/', DescuentosCreateView.as_view(), name='descuento_create'),
    path('descuento/update/<int:pk>/', DescuentosUpdateView.as_view(), name='descuento_update'),
    path('descuento/delete/<int:pk>/', DescuentoDeleteView.as_view(), name='descuento_delete'),

    path('salary/list/', SalaryListView.as_view(), name='salary_list'),
    path('salary/add/', SalaryCreateView.as_view(), name='salary_create'),

    # Vacations
    path('vacations/list/', VacationsListView.as_view(), name='vacations_list'),

    #Company
    path('company/update/', CompanyUpdateView.as_view(), name='company_update')


]
