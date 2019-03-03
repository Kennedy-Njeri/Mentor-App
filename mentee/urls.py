from django.urls import path

from . views import mentee, mentor
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', mentee.home, name="home"),
    path('account/', mentee.account, name="account"),
    path('register/', mentee.register, name="register"),
    path('profile/', mentee.profile, name="profile"),
    path('message/', mentee.MessageCreateView.as_view(), name="Message"),
    path('<int:pk>', mentee.SentDetailView.as_view(), name="sent"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),






    path('account1/', mentor.account1, name="account1"),
    path('register1/', mentor.register1, name="register1"),
    path('profile1/', mentor.profile1, name="profile1"),
]



