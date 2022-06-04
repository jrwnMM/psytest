
from django import forms
from riasec.models import Question

class AddCareerQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question', 'category')

        category_choices = [
            ('R', 'Realistic'),
            ('I', 'Investigative'),
            ('A', 'Artistic'),
            ('S', 'Social'),
            ('E', 'Enterprising'),
            ('C', 'Conventional'),
        ]

        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}, choices=category_choices),
        }