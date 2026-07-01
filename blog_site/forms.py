from .models import Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "input",
            "placeholder": "Enter your email"
        })
    )

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            "class": "input",
            "placeholder": "Choose a username"
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": "Create password"
        })
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "input",
            "placeholder": "Repeat password"
        })
    )

    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

class SearchForm(forms.Form):

    query = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search articles...",
                "class": "input"
            }
        )
    )