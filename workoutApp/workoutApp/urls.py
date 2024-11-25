from django.contrib import admin
from django.urls import path
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from workoutApp.users.views import custom_login_view
from workoutApp.workouts.views import index, about, what_we_do, contacts, login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('about/', about, name='about-us'),
    path('what-we-do/', what_we_do, name='mission'),
    path('contact/', contacts, name='contacts'),
    path('login/', login, name='login'),
    path('workout/', include("workoutApp.workouts.urls")),
    path('nutrition/', include("workoutApp.nutrition.urls")),
    path('users/', include("workoutApp.users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)