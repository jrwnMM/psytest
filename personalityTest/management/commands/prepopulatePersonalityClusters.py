from django.core.management.base import BaseCommand
import joblib
from personalityTest.models import Cluster

class Command(BaseCommand):
    help = 'populate Cluster model'


    def handle(self, *args, **options):
        ml_model = joblib.load("models/personality_model.sav")

        clusters = ml_model.cluster_centers_

        for index, cluster in enumerate(clusters):
            rounded = [ round((x/1)*100, 2) for x in cluster ]
            cluster_model = Cluster()
            cluster_model.cluster = f"Cluster {index + 1}"
            cluster_model.extroversion = rounded[0]
            cluster_model.neurotic = rounded[1]
            cluster_model.agreeable = rounded[2]
            cluster_model.conscientious = rounded[3]
            cluster_model.openness = rounded[4]
            cluster_model.save()


        