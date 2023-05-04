from django.urls import path
from core.erp.views.departaments.view import *

app_name = 'erp'

urlpatterns = [

    path('departaments/list/', DepartamentListView.as_view(), name='departaments_list'),
    path('departaments/create/', DepartamentCreateView.as_view(), name='departaments_create'),
    path('departaments/edit/<int:pk>/', DepartamentUpdateView.as_view(), name='departaments_edit'),
    path('departaments/delete/<int:pk>/', DepartamentDeleteView.as_view(), name='departaments_delete'),
    # path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete')
]

# DepartamentUpdateView