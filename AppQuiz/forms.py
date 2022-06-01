from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from .models import (Answer, Question, Student, StudentAnswer, Subject, User, Profile)


class TeacherSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "text",
        "placeholder": "Username"
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "email",
        "placeholder": "Email"
    }))
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "Password"
    }))
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "Confirm Password"
    }))

    def __init__(self, *args, **kwargs):
        super(TeacherSignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "text",
        "placeholder": "Username"
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "email",
        "placeholder": "Email"
    }))
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "Password"
    }))
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "password",
        "placeholder": "Confirm Password"
    }))

    def __init__(self, *args, **kwargs):
        super(StudentSignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['interests'].label = 'Select Area(s) Of Interest'
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.interests.add(*self.cleaned_data.get('interests'))
        return user


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "text",
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "text",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "text",
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "type": "email",
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "type": "text",
    }))
    class Meta:
        model = Profile
        fields = ['image', 'bio']
