from django.views.generic import TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)


# Create your views here.
class Is_Counselor(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name="Counselor").exists()

class Home(LoginRequiredMixin, Is_Counselor, TemplateView):
    template_name = "administration/admin_home.html"



