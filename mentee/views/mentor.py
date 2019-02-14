from django.shortcuts import render, redirect
from ..models import Status
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import MentorRegisterForm, MentorInterestsForm


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
        form1 = MentorInterestsForm(request.POST)
        if form.is_valid() and form1.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            interests = form1.cleaned_data.get('interests')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')

    else:

        form = MentorRegisterForm()
        form1 = MentorInterestsForm()

    return render(request, 'mentor/register1.html', {'form': form, 'form1': form1})


@login_required
def profile1(request):
    return render(request, 'mentor/profile1.html')
