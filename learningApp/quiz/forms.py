from django import forms
from .models import Quiz, Question, Answer

CORRECT = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'False'), (True, 'True')),
        widget=forms.Select,
    )


class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'length']


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class AddAnswerToQuestionForm(forms.Form):
    first_ans = forms.CharField(max_length=250)
    first_corr = CORRECT
    sec_ans = forms.CharField(max_length=250)
    sec_corr = CORRECT
    third_ans = forms.CharField(max_length=250)
    third_corr = CORRECT
    fourth_ans = forms.CharField(max_length=250)
    fourth_corr = CORRECT


class RegisterForm(forms.Form):
    login = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    confirmation = forms.CharField(max_length=50, widget=forms.PasswordInput)
    email = forms.CharField(max_length=50, widget=forms.EmailInput)
    terms = forms.BooleanField(label="Accept Terms of use")


class LoginForm(forms.Form):
    login = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)