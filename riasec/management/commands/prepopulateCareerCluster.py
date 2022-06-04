from django.core.management.base import BaseCommand
import joblib

from riasec.models import Cluster


class Command(BaseCommand):
    help = "populate Cluster model"

    def handle(self, *args, **options):
        ml_model = joblib.load('models/career_model.sav')

        clusters = ml_model.cluster_centers_

        for index, cluster in enumerate(clusters):
            rounded = [ round((x/1)*100, 2) for x in cluster ]
            cluster_model = Cluster()
            cluster_model.cluster = f"Cluster {index + 1}"
            cluster_model.realistic = rounded[0]
            cluster_model.investigative = rounded[1]
            cluster_model.artistic = rounded[2]
            cluster_model.social = rounded[3]
            cluster_model.enterprising = rounded[4]
            cluster_model.conventional = rounded[5]
            cluster_model.save()
