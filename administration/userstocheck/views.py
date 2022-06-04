from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from administration.forms import ScheduleDateForm

from .forms import SearchForm
from .filters import ProfileFilter
from accounts.models import Profile

from administration.models import AdminScheduledConsultation
from administration.views import SuperUserCheck


class CounselingRequestsView(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = 'userstocheck/counseling-requests.html'
    form_class = SearchForm
    model = Profile
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            self.model.objects
            .exclude(user__username=self.request.user)
            .filter(is_assigned=False)
            .order_by("last_test_taken")
        )
        if qs:
            profiles = ProfileFilter(self.request.GET, queryset=qs)
            return profiles.qs
        else:
            obj = self.model.objects.exclude(user__username=self.request.user)
            qs = obj.filter(is_assigned=False)
            return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            filter=ProfileFilter(self.request.GET, queryset=self.model.objects.all())
        )
        context["form"] = context
        context['schedule_form'] = ScheduleDateForm(initial={
            'managed_by': self.request.user
        })
        return context

class CounselingRequestsSection(CounselingRequestsView):
    template_name = "userstocheck/partials/counseling-requests-section"

class PendingResults(CounselingRequestsView):
    template_name = "userstocheck/pending-results.html"

    def get_queryset(self):
        qs = (
            self.model.objects
            .exclude(user__username=self.request.user)
            .filter(is_result=False)
            .order_by('last_test_taken')
        )
        if qs:
            profiles = ProfileFilter(self.request.GET, queryset=qs)
            return profiles.qs
        else:
            obj_excluded = self.model.objects.exclude(user__username=self.request.user)
            object_list = obj_excluded.filter(is_result=False).order_by('-last_test_taken')
            return object_list

class PendingResultsSection(PendingResults):
    template_name = 'userstocheck/partials/pending-result-section.html'


class AssignedUsers(LoginRequiredMixin, SuperUserCheck, ListView):
    template_name = "userstocheck/assigned-users.html"
    model = AdminScheduledConsultation
    form_class = SearchForm
    context_object_name = "consultations"
    paginate_by = 10

    def get_queryset(self):

        qs = self.model.objects.exclude(managed_by=self.request.user.profile)
        if qs:
            profiles = ProfileFilter(self.request.GET, queryset=qs)
            return profiles.qs
        else:
            return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            filter=ProfileFilter(self.request.GET, queryset=self.model.objects.all())
        )

        context["form"] = context

        return context
