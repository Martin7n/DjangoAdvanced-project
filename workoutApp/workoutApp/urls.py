from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("workoutApp.common.urls")),
    path('workout/', include("workoutApp.workouts.urls")),
    path('nutrition/', include("workoutApp.nutrition.urls")),
    path('accounts/', include("workoutApp.accounts.urls")),
    path('complexes/', include("workoutApp.complexes.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
