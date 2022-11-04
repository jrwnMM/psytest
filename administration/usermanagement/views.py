from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model

from .forms import AdminSearchForm
from .filters import UserFilter

from administration.views import Is_Counselor
User = get_user_model()


class UserManagement(LoginRequiredMixin, Is_Counselor, ListView):
    template_name = "usermanagement/user_management.html"
    model = User
    form_class = AdminSearchForm
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        qs = self.model.objects.exclude(id=self.request.user.id)
        users = UserFilter(self.request.GET, queryset=qs)
        return users.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            filter=UserFilter(self.request.GET, queryset=self.model.objects.all())
        )
        context["users_total"] = self.get_queryset().count()
        context["form"] = context
        return context

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def makesuperuser(request, pk):
    counselor_group = Group.objects.filter(name="Counselor").first()
    user = User.objects.filter(id=pk).first()
    if counselor_group and user:
        user.groups.add(counselor_group)
        user.save()
    return redirect('administration:user-management')

@user_passes_test(lambda u:u.groups.filter(name="Counselor").exists())
def unsuperuser(request, pk):
    counselor_group = Group.objects.filter(name="Counselor").first()
    user = User.objects.filter(id=pk).first()
    if counselor_group and user:
        user.groups.remove(counselor_group)
        user.save()
    return redirect('administration:user-management')