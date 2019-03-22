from django import forms

from django.contrib.auth.models import User

from .models import Subject,  Mentee, Mentor

from django.contrib.auth.forms import UserCreationForm
from .models import Profile


from django.contrib.auth import get_user_model
User = get_user_model()




class MenteeRegisterForm(UserCreationForm):
    email = forms.EmailField()

    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



    def save(self):
        user = super().save(commit=False)
        user.is_mentee = True
        user.save()
        mentee = Mentee.objects.create(user=user)
        mentee.interests.add(*self.cleaned_data.get('interests'))

        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','education']




class MentorRegisterForm(UserCreationForm):
    email = forms.EmailField()

    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def save(self):
        user = super().save(commit=False)
        user.is_mentor = True
        user.save()
        mentor = Mentor.objects.create(user=user)
        mentor.interests.add(*self.cleaned_data.get('interests'))

        return user


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



