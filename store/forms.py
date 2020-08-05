from django import forms
from .models import Listing, Comment, Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('__all__')
        widgets = {
            'listing': forms.HiddenInput(),
            'buyer': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'seller': forms.HiddenInput()
            }

    def __init__(self, *args, **kwargs):
        self.listingStatus = kwargs.pop('status', None)
        self.userAddress = kwargs.pop('address', None)
        self.user = kwargs.pop('user', None)
        self.seller = kwargs.pop('seller', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
    
    def clean(self):

        if self.listingStatus == 4:
            raise forms.ValidationError('Listing has already been sold.')
        elif self.userAddress == None:
            raise forms.ValidationError('You must set a shipping address.')
        elif self.user == self.seller:
            raise forms.ValidationError('Unable to purchase own listing.')

        return self.cleaned_data

class CreateListingForm(forms.ModelForm):
    # gallery = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Listing
        fields = ('__all__')
        widgets = {
            'seller': forms.HiddenInput(),
            'status': forms.HiddenInput(),
            'listing_code': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            }

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
        widgets = {'body': forms.Textarea(attrs={'rows':5,
                                            'cols':70,
                                            'style':'resize:none;'}),
        }

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
        