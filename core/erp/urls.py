from django.urls import path

from core.erp.views.candidate.views import *
from core.erp.views.cuentas.views import AccountsListView
from core.erp.views.departaments.view import *
from core.erp.views.empleados.views.view import *
from core.erp.views.puesto_trabajo.views import *
from core.erp.views.seleccionados.views import *
from core.erp.views.turnos_trabajo.views import *
from core.erp.views.vacante.views import *
from core.erp.views.asistencia.views import *


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
    # path('select/add/', SelectCreateView.as_view(), name='select_create'),
    # path('select/edit/<int:pk>/', SelectUpdateView.as_view(), name='select_update'),
    # path('select/delete/<int:pk>/', SelectDeleteView.as_view(), name='select_delete'),

    # Cuentas
    path('cuentas/list/', AccountsListView.as_view(), name='cuenta_list'),

    # Empleados
    path('empleados/list/', EmpleadoListView.as_view(), name='empleados_list'),
    path('empleados/add/', EmpleadoCreateView.as_view(), name='empleados_create'),
    path('empleados/edit/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleados_update'),
    path('empleados/delete/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleados_delete'),

     # Asistencia
    path('asistencia/list/', AssistanceListView.as_view(), name='asistencia_list'),
    path('asistencia/add/', AssistanceCreateView.as_view(), name='asistencia_create'),
    path('asistencia/update/<str:date_joined>/', AssistanceUpdateView.as_view(), name='asistencia_update'),
    path('asistencia/delete/<str:start_date>/<str:end_date>/', AssistanceDeleteView.as_view(),name='asistencia_delete'),

]
