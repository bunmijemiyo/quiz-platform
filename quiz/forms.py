from django import forms
from .models import Question, AnswerChoice


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class AnswerChoiceForm(forms.ModelForm):
    class Meta:
        model = AnswerChoice
        fields = ['choice', 'text', 'is_correct']


AnswerChoiceFormSet = forms.modelformset_factory(
    AnswerChoice,
    form=AnswerChoiceForm,
    extra=4,  # Number of answer choices you want to provide per question
    can_delete=True,  # Allow forms to be deleted if needed

)

# Override the queryset to return an empty queryset, preventing the display of existing answer choices
AnswerChoiceFormSet.queryset = AnswerChoice.objects.none()


