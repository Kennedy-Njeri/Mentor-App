from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    specialization = models.TextField(blank=True)
    age = models.IntegerField(default=0)
    religion = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)
    website = models.URLField(default='')
    achievements = models.TextField(blank=True)

    def __str__(self):
        return str(self.user)


    def create_profile(sender, **kwargs):
        if kwargs['created']:
            user_profile = UserProfile.objects.create(user=kwargs['instance'])


    post_save.connect(create_profile, sender=User)
