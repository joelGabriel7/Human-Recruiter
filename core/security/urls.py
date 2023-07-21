from django.urls import path
from core.security.views.access_users.views import *
urlpatterns=[
    path('access/user/', AccessUsersListView.as_view(), name="acceso_usuario_list"),
]