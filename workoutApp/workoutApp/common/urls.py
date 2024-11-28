from django.urls import path
from workoutApp.common.views import index, about, what_we_do, contacts

urlpatterns = [
    path('', index, name="index"),
    path('about/', about, name='about-us'),
    path('what-we-do/', what_we_do, name='mission'),
    path('contact/', contacts, name='contacts'),
    ]
