from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.urls import reverse







# Create your models here.


class User(AbstractUser):

    is_mentee = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)



class UserManager(models.Manager):

    def users(self, **kwargs):
        return self.User.objects.all().filter(is_mentor=True)


class Status(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Subject(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name



class Mentee(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Subject, related_name='mentees')


    def __str__(self):
        return self.user.username

class Mentor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Subject, related_name='mentors')


    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    friends = models.ManyToManyField("Profile", blank=True)
    education = models.CharField(default='degree', max_length=100)




    def __str__(self):
        return f'{self.user.username} Profile'



    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)


        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()




class Msg(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True)
    receipient = models.ForeignKey(User, related_name="receipient", on_delete=models.CASCADE)
    msg_content = models.TextField(max_length=100)
    created_at = models.DateField(default=datetime.now, blank=True)
    reply = models.TextField(max_length=100, blank=True)
    replied_at = models.DateField(default=datetime.now, blank=True)

    objects = UserManager()

    def get_absolute_url(self):
        return reverse("list",)

    def __str__(self):
        return "From {}, to {}".format(self.sender.username, self.receipient.username)




