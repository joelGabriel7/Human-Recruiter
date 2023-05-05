from django.urls import path
from core.erp.views.departaments.view import *
from core.erp.views.puesto_trabajo.views import *
from core.erp.views.turnos_trabajo.views import *

app_name = 'erp'

urlpatterns = [
    # Departamentos
    path('departaments/list/', DepartamentListView.as_view(), name='departaments_list'),
    path('departaments/create/', DepartamentCreateView.as_view(), name='departaments_create'),
    path('departaments/edit/<int:pk>/', DepartamentUpdateView.as_view(), name='departaments_edit'),
    path('departaments/delete/<int:pk>/', DepartamentDeleteView.as_view(), name='departaments_delete'),
    # path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete')

    #Puesto_trabajo
    path('puesto/list/', PositionsJobListView.as_view(), name= 'position_list'),
    path('puesto/add/', PositionsJobCreateView.as_view(), name= 'position_create'),
    path('puesto/update/<int:pk>/', PositionsJobUpdateView.as_view(), name= 'position_update'),
    path('puesto/delete/<int:pk>/', PositionsJobDeleteView.as_view(), name= 'position_delete'),

    #Turno trabajo
    path('turno_trabajo/list/', TurnJobListView.as_view(), name='turno_trabajo_list'),
    path('turno_trabajo/add/', TurnJobCreateView.as_view(), name='turno_trabajo_create'),

]

