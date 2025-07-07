from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Project, Task, Profile


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assignees', 'due_date', 'status']
        widgets = {
            'assignees': forms.CheckboxSelectMultiple(),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )

    class Meta:
        model = User
        # include email in the order you want fields rendered
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        # pull the cleaned email into the user object
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("That email is already in use.")
        return email

class UserProfileForm(UserChangeForm):
    password = None  # hide the default password field
    class Meta(UserChangeForm.Meta):
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

class PasswordForm(PasswordChangeForm):
    pass