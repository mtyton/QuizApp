from django import forms
from .models import Quiz, Question, Answer


class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'length']


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']


class AddAnswerToQuestionForm(forms.Form):
    Correct = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'False'), (True, 'True')),
        widget=forms.Select,
    )
    first_ans = forms.CharField(max_length=250)
    first_corr = Correct
    sec_ans = forms.CharField(max_length=250)
    sec_corr = Correct
    third_ans = forms.CharField(max_length=250)
    third_corr = Correct
    fourth_ans = forms.CharField(max_length=250)
    fourth_corr = Correct


class RegisterForm(forms.Form):
    login = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    confirmation = forms.CharField(max_length=50, widget=forms.PasswordInput)
    email = forms.CharField(max_length=50, widget=forms.EmailInput)
    terms = forms.BooleanField(label="Accept Terms of use")


class LoginForm(forms.Form):
    login = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
