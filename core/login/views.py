import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, FormView
import config.settings as setting
from config import settings
from core.user.models import User
from .form import ResetPasswordForm, ChangePasswordForm


class LoginHumanRecruiterView(LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio de Sesion'
        return context


class LogoutHumanRecruiterView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class LoginResetPasswordView(FormView):
    template_name = 'reset_password.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def send_email_reset_password(self, user):
        data = {}
        try:

            url = settings.DOMAIN if not setting.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()

            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            email_to = user.email

            messages = MIMEMultipart("""Este es el mensaje de las narices""")
            messages['From'] = settings.EMAIL_HOST_USER
            messages['To'] = email_to
            messages['Subject'] = "Solicitud de cambio de contraseña"

            content = render_to_string('login/send_email.html', {
                'user': user,
                'link_resetpwd': f'http://{url}/login/change/password/{str(user.token)}/',
                'link_home': f'http://{url}'
            })
            # content = render_to_string('send_email.html', {'user': User.objects.get(pk=1)})
            messages.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER, email_to, messages.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                user = form.get_user()
                data = self.send_email_reset_password(user)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de contraseña'
        return context


class ChangePasswordView(FormView):
    template_name = 'change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return super().get(self, request, *args, **kwargs)
        return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
            else:
                data['error']= form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cambio de contraseña'
        return context
