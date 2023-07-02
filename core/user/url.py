from django.urls import path
from core.user.views import *

app_name = 'user'

urlpatterns = [
    # Puesto_trabajo
    path('list/', UserListView.as_view(), name='user_list'),
    path('add/', UserCreateView.as_view(), name='user_create'),
    # path('puesto/update/<int:pk>/', PositionsJobUpdateView.as_view(), name='position_update'),
    # path('puesto/delete/<int:pk>/', PositionsJobDeleteView.as_view(), name='position_delete'),
]