from django.shortcuts import render, redirect,  get_object_or_404
from ..models import Status
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import MentorRegisterForm

from django.http import HttpResponseRedirect
from ..models import Profile


from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.





def home(request):

    return render(request, 'home.html')


def account1(request):

    context = {

        'statuses': Status.objects.all()

    }

    return render(request, 'mentor/account1.html', context)

def register1(request):

    if request.method == 'POST':

        form = MentorRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')

    else:

        form = MentorRegisterForm()


    return render(request, 'mentor/register1.html', {'form': form})


@login_required
def profile1(request):
    return render(request, 'mentor/profile1.html')



