from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

from .models import UserAddress, CustomUser
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm, CustomUserChangeForm, ChangeAddressForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = self.request.user
        group = Group.objects.get(name='customer')
        return super(SignUpView, self).form_valid(form)
        user.groups.add(group)

def userProfileView(request):
    user = request.user

    try:
        # Grab user object from CustomerUser
        userAddress = UserAddress.objects.get(user__id=user.id)
        form_address = ChangeAddressForm(instance=userAddress)
    except UserAddress.DoesNotExist:
        userAddress = None
        form_address = ChangeAddressForm()

    if request.method == "POST":
        form_user = CustomUserChangeForm(request.POST, instance=user, files=request.FILES)
        form_address = ChangeAddressForm(request.POST, instance=userAddress)
        if form_user.is_valid() and form_address.is_valid():
            form_user.save()
            obj = form_address.save(commit=False)
            obj.user = user
            obj.save()
            return redirect('user-profile')
    else:
        form_user = CustomUserChangeForm(instance=user)
        
    context = {
        'form_user': form_user,
        'form_address': form_address,
        'user': user,
    }
    return render(request, 'user_profile.html', context)