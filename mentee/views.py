from django.shortcuts import render, redirect
from mentee.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
# Create your views here.

def home(request):

    return render(request, 'home.html')




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegistrationForm()

        args = {'form': form}

        return render(request, 'register.html', args)



def profile(request):

    user = User.objects.get(is_staff= False)
    #args = {'user': request.user }

    args = {
        'user': user
    }

    return render(request, 'profile.html', args)



def edit_profile(request):


    if request.method == 'POST':

        form = UserChangeForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:


        form = UserChangeForm(instance=request.user)

        args = {'form': form}

        return render(request, 'edit_profile.html', args)



def login(request):

    return render(request, 'login.html')