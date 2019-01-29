from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('profile', views.profile, name="profile"),
    path('profile/edit', views.edit_profile, name="edit_profile")


]