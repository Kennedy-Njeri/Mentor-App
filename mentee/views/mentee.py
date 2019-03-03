from django.shortcuts import render, redirect, get_object_or_404
from ..models import Status
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import MenteeRegisterForm,UserUpdateForm, ProfileUpdateForm
from django.views.generic import TemplateView
from ..models import Profile, Msg
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponseRedirect

from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)

from django.urls import reverse_lazy
from .. import models


# Create your views here.




def home(request):

    return render(request, 'home.html')


def account(request):

    users = User.objects.all().filter(is_mentor=True)

    context = {

        'users': users


    }

    return render(request, 'menti/account.html', context)

def register(request):

    if request.method == 'POST':

        form = MenteeRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')

    else:

        form = MenteeRegisterForm()


    return render(request, 'menti/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {

        'u_form': u_form,
        'p_form': p_form
    }


    return render(request, 'menti/profile.html', context)



class MessageCreateView(CreateView):

    fields = ('receipient', 'msg_content')
    model = Msg
    template_name = 'menti/messagecreate.html'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)





class SentDetailView(DetailView):
    model = Msg
    context_object_name = 'messo'
    template_name = 'menti/sent.html'



    def get_queryset(self):
        return self.model.objects.filter(sender=self.request.user)




