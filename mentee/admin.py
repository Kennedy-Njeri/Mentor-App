from django.contrib import admin
from .models import Subject, Mentee, Mentor , User, Profile, Msg
# Register your models here.




class MsgAdmin(admin.ModelAdmin):


    search_fields = ("msg_content",)

    list_filter = ("is_approved",)

    list_display = ("sender", "receipient", "sent_at", "msg_content", "comment", "comment_at", "is_approved", "date_approved")

    list_editable = ("is_approved",)









admin.site.register(Subject)

admin.site.register(Mentee)

admin.site.register(Mentor)

admin.site.register(User)

admin.site.register(Profile)

admin.site.register(Msg, MsgAdmin)

