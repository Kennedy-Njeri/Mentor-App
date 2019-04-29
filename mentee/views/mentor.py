from django.shortcuts import render, redirect,  get_object_or_404
#from ..models import Status
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import MentorRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)

from django.http import HttpResponseRedirect
from ..models import Profile

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.views.generic import TemplateView
from ..models import Profile, Msg
from django.db.models import Count, Q

from django.urls import reverse_lazy
from ..forms import ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


from django.contrib.auth import get_user_model
User = get_user_model()




"""Landing page """

def home(request):

    return render(request, 'home.html')



"""For Mentor Account"""

class AccountView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_mentor


    def get(self, request):

        return render(request, 'mentor/account1.html', )



"""Registration for mentors"""

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



def profile1(request):

    if not request.user.is_mentor:
        return redirect('home')

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


"""Login function"""
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('account1'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'mentor/login1.html', {})




"""controls messege view"""
class MessageView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'mentor/messages-module1.html'
    model = Msg

    def test_func(self):
        return self.request.user.is_mentor


    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        context['count'] = Msg.objects.filter(receipient=self.request.user).filter(is_approved=False).count()
        context['count1'] = Msg.objects.filter(receipient=self.request.user).filter(is_approved=True).count()
        #context['count'] = Msg.objects.annotate(Count(is_approved=True))

        return context

    def get_queryset(self):
        return self.model.objects.filter(receipient=self.request.user)





"""Creates new message"""

class MessageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    fields = ('receipient', 'msg_content')
    model = Msg
    template_name = 'mentor/messagecreate1.html'

    def test_func(self):
        return self.request.user.is_mentor

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('list1')


"""List sent Messages"""
class MessageListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = Msg
    template_name = 'mentor/listmessages1.html'
    context_object_name = 'sentmesso'

    def test_func(self):
        return self.request.user.is_mentor

    def get_queryset(self):
        return self.model.objects.filter(sender=self.request.user)


"""details the message sent"""

class SentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    model = Msg
    context_object_name = 'messo'
    template_name = 'mentor/sent1.html'

    def test_func(self):
        return self.request.user.is_mentor

    def get_queryset(self):
        return self.model.objects.filter(sender=self.request.user)

"""Deletes sent messages"""
class SentMessageDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Msg
    success_url = reverse_lazy("list1")
    template_name = 'mentor/sentmessage_delete1.html'

    def test_func(self):
        return self.request.user.is_mentor



""" Lists messages in inbox view"""

class InboxView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    def test_func(self):
        return self.request.user.is_mentor

    model = Msg
    context_object_name = 'inbox'
    template_name = 'mentor/inbox1.html'



    def get_queryset(self):
        return self.model.objects.filter(receipient=self.request.user).filter(is_approved=False)


"""Inbox Detailed view"""
class InboxDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    model = Msg
    context_object_name = 'messo'
    template_name = 'mentor/inboxview1.html'

    def test_func(self):
        return self.request.user.is_mentor


    def get_queryset(self):
        return self.model.objects.filter(receipient=self.request.user)



"""Replies, approves, comments on messages"""
def reply_message(request, pk):

    if not request.user.is_mentor:
        return redirect('home')


    reply = get_object_or_404(Msg, pk=pk)

    if request.method == 'POST':

        form = ReplyForm(request.POST)

        if form.is_valid():

            reply.is_approved = form.cleaned_data['is_approved']
            reply.comment = form.cleaned_data['comment']
            reply.save()

            return redirect('inbox2')

    else:

            form = ReplyForm

    context = {
                'reply': reply,
                'form' : form,
            }

    return render(request, 'mentor/comment.html', context)


"""view list of approved messeges from mentors"""
class Approved(LoginRequiredMixin, UserPassesTestMixin, ListView):

    def test_func(self):
        return self.request.user.is_mentor

    #def get(self, request):

        #messo = Msg.objects.filter(is_approved=True).order_by('-date_approved')

        #context = {

           # 'messo': messo,

        #}

        #return render(request, "menti/approved.html", context)

    model = Msg.objects.filter(is_approved=True).order_by('-date_approved')

    template_name = 'mentor/approved.html'

    context_object_name = 'messo'


    def get_queryset(self):

        return self.model.filter(receipient=self.request.user)


"""view details of a user in the profile"""

class ProfileDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    model = Msg
    context_object_name = 'msg'
    template_name = 'mentor/profile_detail1.html'

    def test_func(self):
        return self.request.user.is_mentor



