from django.contrib import admin
from .models import Status, Subject, Mentee, Mentor , User, Profile
# Register your models here.

admin.site.register(Status)

admin.site.register(Subject)

admin.site.register(Mentee)

admin.site.register(Mentor)

admin.site.register(User)

admin.site.register(Profile)