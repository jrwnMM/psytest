from django import forms
from personalityTest.models import Question

class AddPQuestionsForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question', 'category', 'key')

        category_choices = [
            ('EXT', 'Extroversion'),
            ('EST', 'Neurotic'),
            ('AGR', 'Agreeable'),
            ('CSN', 'Conscientious'),
            ('OPN', 'Openness'),
        ]

        key_choices = [
            ('1', 'Positive'),
            ('0', 'Negative')
        ]

        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'rows': 5}),
        }