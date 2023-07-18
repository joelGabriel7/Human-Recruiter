from django.urls import path
from core.login.views import *
urlpatterns=[
    path('', LoginHumanRecruiterView.as_view(), name="login"),
    path('logout/', LogoutHumanRecruiterView.as_view(), name="logout"),
    path('reset/password/', LoginResetPasswordView.as_view(), name="reset_password"),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name="change_password"),
]