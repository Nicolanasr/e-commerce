from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = False

    def clean(self):
       email = self.cleaned_data.get('email')
       username = self.cleaned_data.get('username')
       if User.objects.filter(email=email).exists():
            raise ValidationError("Email Already exists")
       elif User.objects.filter(username=username).exists():
            raise ValidationError("Username Already exists")
       return self.cleaned_data


class ChangeUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email']

    # def clean(self):
    #    email = self.cleaned_data.get('email')
    #    if User.objects.filter(email=email).exists():
    #         raise ValidationError("Email Already exists")
    #    return self.cleaned_data
