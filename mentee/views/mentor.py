from django.shortcuts import render, redirect,  get_object_or_404
from ..models import Status
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import MentorRegisterForm, UserUpdateForm, ProfileUpdateForm

from django.http import HttpResponseRedirect
from ..models import Profile


from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.





def home(request):

    return render(request, 'home.html')


def account1(request):



    return render(request, 'mentor/account1.html',)


def login1(request):

    return render(request, 'mentor/account1.html')




def register1(request):

    if request.method == 'POST':

        form = MentorRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login1')

    else:

        form = MentorRegisterForm()


    return render(request, 'mentor/register1.html', {'form': form})


@login_required
def profile1(request):
    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been Updated!')
            return redirect('profile1')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {

        'u_form': u_form,
        'p_form': p_form
    }


    return render(request, 'mentor/profile1.html', context)



