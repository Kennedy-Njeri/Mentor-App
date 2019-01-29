
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('mentee.urls')),
    #path('/mentor', include('mentor.urls')),
    path('admin/', admin.site.urls),
]
