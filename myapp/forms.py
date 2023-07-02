from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)

from .models import Talk

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "icon")

class MailSettingForm(forms.ModelsForm):
    pass


class MailSettingForm(forms.ModelsForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "新しいユーザー名"}

class ImageSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("icon",)

class TalkForm(forms.ModelForm):

    class Meta:
        model = Talk
        fields = ("talk",)
        widgets = {"talk": forms.TextInput(attrs={"autocomplete": "off"})}