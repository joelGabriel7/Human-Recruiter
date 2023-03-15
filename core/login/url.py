from django.urls import path
from core.login.views import *
urlpatterns=[
    path('', LoginHumanRecruiterView.as_view(), name="login"),
    path('logout/', LogoutHumanRecruiterView.as_view(), name="logout")
]