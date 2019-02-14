from django.shortcuts import render, redirect
from ..models import Status
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import MenteeRegisterForm,UserUpdateForm, ProfileUpdateForm


from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.




def home(request):

    return render(request, 'home.html')


def account(request):

    context = {

        'statuses': Status.objects.all()

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
