from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Weighting

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class WeightingForm(forms.ModelForm):
    class Meta:
        model = Weighting
        fields = ['animal', 'weighing_date', 'weight_in_kg']
