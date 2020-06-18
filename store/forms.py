from django import forms
from .models import Listing, Comment, Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        self.listingStatus = kwargs.pop('status', None)
        self.userAddress = kwargs.pop('address', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        if self.listingStatus == 4:
            raise forms.ValidationError('Listing has already been sold.')
        elif self.userAddress == None:
            raise forms.ValidationError('You must set a shipping address.')
        return self.cleaned_data

class CreateListingForm(forms.ModelForm):
    gallery = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'multiple': True}))

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
        