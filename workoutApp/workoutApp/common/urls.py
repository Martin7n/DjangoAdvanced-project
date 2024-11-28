from django.urls import path
from workoutApp.common.views import index, about, what_we_do, contacts, login

urlpatterns = [
    path('', index, name="index"),
    path('about/', about, name='about-us'),
    path('what-we-do/', what_we_do, name='mission'),
    path('contact/', contacts, name='contacts'),
    path('login/', login, name='login'),
    ]
