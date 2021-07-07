from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        required=True
    )

    first_name = forms.CharField(
        widget=forms.TextInput(),
        label="First Name",
        max_length=25,
        required=True
    )

    last_name = forms.CharField(
        widget=forms.TextInput(),
        label="Last Name",
        max_length=25,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name','password1', 'password2']
