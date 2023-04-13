import django_filters
from iqtest.models import Result as IQResult

class IQFilter(django_filters.FilterSet):
    date_created = django_filters.DateFromToRangeFilter(field_name='date_created', lookup_expr='year')
    class Meta:
        model = IQResult
        fields = ["user__user__first_name", "result"]