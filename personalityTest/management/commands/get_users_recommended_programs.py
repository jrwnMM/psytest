from django.core.management.base import BaseCommand
from personalityTest.models import RecommendedProgram, Result as PResult
import joblib

from riasec.models import OfferedProgram


class Command(BaseCommand):
    help = "populate Cluster model"

    def handle(self, *args, **options):
        personality_results = PResult.objects.all()

        for result in personality_results:

            personality = [[
                        result.extroversion,
                        result.neurotic,
                        result.agreeable,
                        result.conscientious,
                        result.openness,
                    ]]
            
            program_prediction = self.program_predictor(personality)
            first_ranked = self.first_ranked(program_prediction)

            programs = []
            for key, value in first_ranked.items():
                try: 
                    offeredPrograms = OfferedProgram.objects.filter(interest=key)
                    if offeredPrograms:
                        for item in offeredPrograms:
                            programs.append(item)
                except OfferedProgram.DoesNotExist:
                    pass
            
            
            if programs:
                if RecommendedProgram.objects.filter(user=result.user).exists():
                    RecommendedProgram.objects.filter(user=result.user).delete()

                for obj in set(programs):
                    recCareer = RecommendedProgram()
                    recCareer.user = result.user
                    recCareer.offeredProgram = obj
                    recCareer.save()

    def program_predictor(self, personality):
        model = joblib.load("models/personality_career_dt.sav")
        prediction = model.predict(personality)
        return prediction

    def first_ranked(self, prediction):
        first = {}
        
        obj = {
        'realistic' : prediction[0][0],
        'investigative' : prediction[0][1],
        'artistic' : prediction[0][2],
        'social' : prediction[0][3],
        'enterprising' : prediction[0][4],
        'conventional' : prediction[0][5]
        }

        sorted_obj = {key: value for key, value in sorted(obj.items(), key=lambda item: item[1], reverse=True)}

        for key, value in sorted_obj.items():
            if list(sorted_obj.values())[0] == value:
                first[key] = value
        
        return first
