from django import forms
from forum.models import Question, Answer, UserProfile

class CreateQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name','desc','img','topic')

class AnswerQuestion(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('ans','img')

class UserProfileForm(forms.ModelForm):
    class Meta:
            model = UserProfile
            fields = ('avatar',)