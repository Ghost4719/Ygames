# forms.py

from django import forms
from .models import Game
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


from django import forms
from django.contrib.auth.models import User

class CustomUserChangeForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False, label="New Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False, label="Confirm New Password")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Skip uniqueness check if the username is not changing
        if username and username != self.instance.username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("A user with that username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Ensure that the passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        password1 = self.cleaned_data.get("password1")
        if password1:  # If password1 is provided, set the new password
            user.set_password(password1)

        if commit:
            user.save()

        return user






    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['username'].initial = self.instance.username
            self.fields['email'].initial = self.instance.email

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'cover_image', 'file', 'pic', 'genre', 'howto', 
                  'bg_color', 'text_color', 'link_color', 'font_family', 'font_size', 
                  'banner_image', 'background_image', 'bg_style']

        widgets = {
            'description': forms.Textarea(attrs={'class': 'ckeditor'}),
            'howto': forms.Textarea(attrs={'class': 'ckeditor'}),
            'bg_color': forms.TextInput(attrs={'type': 'color'}),
            'text_color': forms.TextInput(attrs={'type': 'color'}),
            'link_color': forms.TextInput(attrs={'type': 'color'}),
            'font_family': forms.Select(choices=[('lato', 'Lato'), ('serif', 'Serif'), ('sans_serif', 'Sans Serif'), 
                                                 ('pixel', 'Pixel'), ('anonymous_pro', 'Anonymous Pro')]),
            'font_size': forms.Select(choices=[('small', 'Small'), ('medium', 'Medium'), 
                                               ('large', 'Large'), ('very_large', 'Very Large')]),
        }
