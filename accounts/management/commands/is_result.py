from django.core.management.base import BaseCommand, CommandError
from dateutil.relativedelta import relativedelta
from datetime import datetime
from accounts.models import Profile

class Command(BaseCommand):
    help = 'populate age in Profile model'


    def handle(self, *args, **options):
        users = Profile.objects.all()
        for user in users:
            if user.is_assigned == None:
                # print(user.is_assigned, user.is_result)
                user.is_result = None
                user.save()
