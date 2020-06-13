from django import forms
from .models import Listing, Comment


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('__all__')

    class FileFieldForm(forms.Form):
        file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        # instance = kwargs.get('instance', None)
        self.loggedUser = kwargs.pop('user', None)
        super(CreateListingForm, self).__init__(*args, **kwargs)

        # if instance:
        #     self.initial['seller'] = instance.seller

    def clean_seller(self):
        # instance_user = int(self.instance.seller.id)
        form_user = self.cleaned_data['seller']
        logged_user = self.loggedUser

        # print('formuser', form_user)
        # print('loggeduser', logged_user)
        # print('instanceuser', instance_user)

        if (form_user != logged_user):
            raise forms.ValidationError('Invalid listing creation by current user')
        return form_user

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, *args, **kwargs):
        self.loggedUser = kwargs.pop('user', None)
        self.listing = kwargs.pop('listing', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean_author(self):
        form_user = self.cleaned_data['author']
        logged_user = self.loggedUser

        if (form_user != logged_user):
            raise forms.ValidationError('Comment submitted by invalid user.')

    def clean_listing(self):
        form_listing = self.cleaned_data['listing']
        current_listing = self.listing

        if (form_listing != current_listing):
            raise forms.ValidationError('Comment submitted to invalid listing.')
        