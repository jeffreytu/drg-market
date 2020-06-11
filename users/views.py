from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm, CustomUserChangeForm

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
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile')
    form = CustomUserChangeForm(instance=user)
    context = {
        'form': form
    }
    return render(request, 'user_profile.html', context)