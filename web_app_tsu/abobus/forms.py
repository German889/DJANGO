from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Project
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class RegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('STUDENT', 'Student'),
        ('INVESTOR', 'Investor'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect)
    name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'name', 'last_name')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.save()
        profile = Profile.objects.create(user=user, user_type=self.cleaned_data['user_type'],
                                          name=self.cleaned_data['name'], last_name=self.cleaned_data['last_name'])
        if commit:
            profile.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'payback_period', 'goals', 'intended_outcome']
