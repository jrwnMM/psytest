from django.core.management.base import BaseCommand, CommandError
from dateutil.relativedelta import relativedelta
from datetime import datetime
from accounts.models import Profile

class Command(BaseCommand):
    help = 'populate age in Profile model'


    def handle(self, *args, **options):
        users = Profile.objects.all()
        for user in users:
            if user.date_of_birth:
                user.age = relativedelta(datetime.today(),user.date_of_birth).years