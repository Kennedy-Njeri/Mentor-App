from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from PIL import Image



# Create your models here.



# Create your models here.


class User(AbstractUser):



    is_mentee = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)



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
    interests = models.ManyToManyField(Subject,related_name='interested_mentee')

    def __str__(self):
        return self.user.username

class Mentor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    interests = models.ManyToManyField(Subject,related_name='interested_mentor')

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)


        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)