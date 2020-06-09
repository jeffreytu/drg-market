from django import forms
from .models import Listing, Comment


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        self.loggedUser = kwargs.pop('user', None)
        super(CreateListingForm, self).__init__(*args, **kwargs)

    def clean_seller(self):
        form_user = self.cleaned_data['seller']
        logged_user = self.loggedUser

        if (form_user != logged_user):
            raise forms.ValidationError('Invalid listing creation by current user')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'body')