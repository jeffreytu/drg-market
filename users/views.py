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
        group = Group.objects.get(name='customer')
        self.object.groups.add(group)
        return super(SignUpView, self).form_valid(form)

def userProfileView(request):
    user = request.user
    # Grab user object from CustomerUser
    userAddress = UserAddress.objects.get(user__id=user.id)
    if request.method == "POST":
        form_user = CustomUserChangeForm(request.POST, instance=user)
        form_address = ChangeAddressForm(request.POST, instance=userAddress)
        if form_user.is_valid() and form_address.is_valid():
            form_user.save()
            form_address.save(commit=False)
            form_address.user = user
            form_address.save()
            return redirect('user-profile')
    form_user = CustomUserChangeForm(instance=user)
    form_address = ChangeAddressForm(instance=userAddress)
    context = {
        'form_user': form_user,
        'form_address': form_address
    }
    return render(request, 'user_profile.html', context)