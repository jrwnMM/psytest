from django.views.generic import TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)


# Create your views here.
class SuperUserCheck(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class Home(LoginRequiredMixin, SuperUserCheck, TemplateView):
    template_name = "administration/admin_home.html"



