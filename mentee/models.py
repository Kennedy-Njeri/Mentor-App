from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    is_mentee = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interest = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username


class Mentee(models.Model):
    """Mentee models"""

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    # interests = models.OneToOneField(Subject, related_name='mentees', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Mentor(models.Model):
    """Mentor models"""

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)

    # interests = models.OneToOneField(Subject, related_name='mentors', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    """Profile Model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    education = models.CharField(default='degree', max_length=100)
    registration = models.CharField(default='BBIT/2014/62324', max_length=100)

    def __str__(self):
        return f'{self.user.username} '

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


class Reply(models.Model):
    """Reply Model"""

    sender = models.ForeignKey(User, related_name="sender2", on_delete=models.CASCADE, null=True)
    reply = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    conversation = models.ForeignKey('Conversation', related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return "From {}, in {}".format(self.sender.username, self.conversation)

    def save(self, *args, **kwargs):
        if self.reply and self.replied_at is None:
            self.replied_at = now()

        super(Reply, self).save(*args, **kwargs)


class Conversation(models.Model):
    """Conversation Model"""

    sender = models.ForeignKey(User, related_name="sender1", on_delete=models.CASCADE, null=True)
    receipient = models.ForeignKey(User, related_name="receipient1", on_delete=models.CASCADE)
    conversation = models.TextField(max_length=100)
    sent_at = models.DateTimeField(null=True, blank=True)

    # reply = models.TextField(blank=True, null=True)
    # replied_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-sent_at']

    @property
    def get_replies(self):
        return self.replies.all()

    def __str__(self):
        return "From {}, to {}".format(self.sender.username, self.receipient.username)

    def save(self, *args, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()

        # if (self.reply and self.replied_at is None):
        # self.replied_at = now()

        super(Conversation, self).save(*args, **kwargs)


class Msg(models.Model):
    """Message Model"""

    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True)
    receipient = models.ForeignKey(User, related_name="receipient", on_delete=models.CASCADE)
    msg_content = models.TextField(max_length=100)
    sent_at = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    comment_at = models.DateTimeField(blank=True, null=True)
    is_approved = models.BooleanField(default=False, verbose_name="Approve?")
    date_approved = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "From {}, to {}".format(self.sender.username, self.receipient.username)

    def save(self, *args, **kwargs):
        if not self.id:
            self.sent_at = timezone.now()

        if self.comment and self.date_approved is None:
            self.date_approved = now()

        if self.comment and self.comment_at is None:
            self.comment_at = now()

        super(Msg, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-sent_at']
