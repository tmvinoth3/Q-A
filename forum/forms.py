from django import forms
from forum.models import Question, Answer

class CreateQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name','img','topic')

class AnswerQuestion(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('ans','img')