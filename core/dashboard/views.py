from django.views.generic import TemplateView


# Create your views here.

class DashboardView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Human Recruiter'
        return context