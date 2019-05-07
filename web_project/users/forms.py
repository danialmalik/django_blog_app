from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import Profile
from .settings import DATE_INPUT_FORMAT


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=100, help_text='Required. Inform a valid email address.')

    def clean(self):
        cleaned_data = self.cleaned_data
        # rename 'password1' field to 'password'
        cleaned_data['password'] = cleaned_data['password1']
        # delete 'password1' amd 'password2' fields which were for only validation
        # purposes.
        del cleaned_data['password1']
        del cleaned_data['password2']
        return cleaned_data

    def save(self, commit=True):
        raw_password = self.cleaned_data['password']

        user = User(**self.cleaned_data)
        user.set_password(raw_password)
        user.save()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    # chrome uses this date format
    birthday = forms.DateField(widget=forms.DateInput(format=DATE_INPUT_FORMAT,
                                                      attrs={
                                                          'type': 'date'
                                                      }))

    class Meta:
        model = Profile
        fields = ('profile_picture', 'address', 'birthday')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')
