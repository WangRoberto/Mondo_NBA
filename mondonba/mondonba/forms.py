from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.forms import ModelForm
from gestione.models import Product

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=20, help_text='Required', label=("Username"), widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(max_length=50, help_text='Required', label=("Email"), widget=forms.TextInput(attrs={"placeholder":"Email", "type":"email"}))
    password1 = forms.CharField(max_length=20, help_text='Required', label=("password1"), widget=forms.TextInput(attrs={"placeholder":"Password", "type":"password"}))
    password2 = forms.CharField(max_length=20, help_text='Required', label=("password2"), widget=forms.TextInput(attrs={"placeholder":"Confirm Password", "type":"password"}))
    usable_password = None
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "stext-111 cl2 plh3 size-116 p-l-62 p-r-30"

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "stext-111 cl2 plh3 size-116 p-l-62 p-r-30"

    username = forms.CharField(max_length=20, help_text='Required', label=("Username"),
                               widget=forms.TextInput(attrs={"placeholder": "Username"}))

    password = forms.CharField(max_length=20, help_text='Required', label=("password"),
                                widget=forms.TextInput(attrs={"placeholder": "Password", "type": "password"}))


