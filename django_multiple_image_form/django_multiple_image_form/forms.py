from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(required=True, max_length=25, help_text='Required.')
    last_name = forms.CharField(required=True, max_length=25, help_text='Required.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['email'].label = 'Email Address'






