def populate_models(sender, **kwargs):
    from django.contrib.auth.models import Group
    counselor_group, created = Group.objects.get_or_create(name="Counselor")