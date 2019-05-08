from django import forms

from django.contrib.auth.models import User

from .models import Mentee, Mentor, UserInfo

from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Msg
from django.forms import ModelForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField


from django.contrib.auth import get_user_model
User = get_user_model()




class MenteeRegisterForm(UserCreationForm):

    email = forms.EmailField()

    #interests = forms.ModelMultipleChoiceField(
        #queryset=Subject.objects.all(),
        #widget=forms.CheckboxSelectMultiple,
        #required=True)

    #interests= forms.ChoiceField(required=True, widget=forms.RadioSelect(
        #attrs={'class': 'Radio'}))

    class Meta:
       model = User
       fields = ['username', 'email', 'password1', 'password2']



    def save(self):
        user = super().save(commit=False)
        user.is_mentee = True
        user.save()
        mentee = Mentee.objects.create(user=user)
        #mentee.interests.add(*self.cleaned_data.get('interests'))
        #mentee.interests = self.cleaned_data.get('interests')

        return user


class UserInfoForm(forms.ModelForm):

    interest = forms.ChoiceField(required=True, widget=forms.RadioSelect(
        attrs={'class': 'Radio'}), choices=(('economics', 'Economics'), ('bbit', 'BBIT'),))

    class Meta():
        model = UserInfo
        fields = ('interest',)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','education', 'registration']




class MentorRegisterForm(UserCreationForm):
    email = forms.EmailField()

    #interests = forms.ModelMultipleChoiceField(
        #queryset=Subject.objects.all(),
        #widget=forms.CheckboxSelectMultiple,
        #required=True
    #)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def save(self):
        user = super().save(commit=False)
        user.is_mentor = True
        user.save()
        mentor = Mentor.objects.create(user=user)
        #mentor.interests.add(*self.cleaned_data.get('interests'))

        return user


class UserInfoForm(forms.ModelForm):

    interest = forms.ChoiceField(required=True, widget=forms.RadioSelect(
        attrs={'class': 'Radio'}), choices=(('economics', 'Economics'), ('bbit', 'BBIT'),))

    class Meta():
        model = UserInfo
        fields = ('interest',)


class ReplyForm(forms.Form):

    is_approved = forms.BooleanField(

        label='Approve?',
        help_text='Are you satisfied with the request?',
        required=False,

    )

    comment = forms.CharField(

        widget=forms.Textarea,
        min_length=4,
        error_messages={

            'required': 'Please enter your reply or comments',
            'min_length': 'Please write at least 5 characters (you have written %(show_value)s)'

        }

    )

class SendForm(ModelForm):

    class Meta:
        model = Msg
        fields = ['msg_content']







