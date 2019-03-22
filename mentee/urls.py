from django.urls import path

from . views import mentee, mentor
from django.contrib.auth import views as auth_views




urlpatterns = [

    path('', mentee.home, name="home"),

    #mentee url
    path('account/', mentee.account, name="account"),
    path('register/', mentee.register, name="register"),
    path('profile/', mentee.profile, name="profile"),
    #path('message-module/', mentee.MessageView.as_view(), name="module-message"),
    path('message-module/', mentee.messege_view, name="module-message"),
    path('message/', mentee.MessageCreateView.as_view(), name="Message"),
    path('<int:pk>', mentee.SentDetailView.as_view(), name="sent"),
    path('inbox/<int:pk>', mentee.InboxDetailView.as_view(), name="detail-inbox"),
    path('reply/<int:pk>', mentee.ReplyCreateView.as_view(), name="reply"),
    #path('login/', auth_views.LoginView.as_view(template_name='menti/login.html'), name='login'),
    path('login/', mentee.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='menti/logout.html'), name='logout'),
    path('list-message/', mentee.MessageListView.as_view(), name='list'),
    path('inbox-message/', mentee.InboxView.as_view(), name='inbox1'),
    path('delete/<int:pk>', mentee.SentMessageDelete.as_view(), name='delete'),





    #mentor urls
    path('account1/', mentor.account1, name="account1"),
    path('register1/', mentor.register1, name="register1"),
    path('profile1/', mentor.profile1, name="profile1"),
    #path('login1/', mentor.login1, name="login1"),
    path('login1/', mentor.user_login, name='login1'),
    path('logout1/', auth_views.LogoutView.as_view(template_name='mentor/logout1.html'), name='logout1'),
    path('message-module1/', mentor.MessageView.as_view(), name="module-message1"),
    path('message-mentor/', mentor.MessageCreateView.as_view(), name="Message1"),
    path('inbox-message1/', mentor.InboxView.as_view(), name='inbox1'),
    path('inbox-mentor/<int:pk>', mentor.InboxDetailView.as_view(), name="detail-inbox1"),
    path('list-message1/', mentor.MessageListView.as_view(), name='list1'),
    path('delete-mentor/<int:pk>', mentor.SentMessageDelete.as_view(), name='delete'),


]



