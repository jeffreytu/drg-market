from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserAddress
from django.views.generic.edit import FormMixin

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

class ChangeAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = ('__all__')
        exclude = ['user']

    def clean(self):
        print(self)
