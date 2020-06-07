from django.shortcuts import render
from django.contrib.auth.models import User, Group

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        group = Group.objects.get(name='customer')
        self.object.groups.add(group)
        return super(SignUpView, self).form_valid(form)