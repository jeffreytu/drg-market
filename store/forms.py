from django import forms
from .models import Listing

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('__all__')