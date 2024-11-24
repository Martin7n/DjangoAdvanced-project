from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import RegisterView, custom_login_view, user_profile_view, CustomUserEditView, view_profile, delete_profile, \
    view_all_profile, custom_logout

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', custom_login_view, name='login'),
    path('profile/', user_profile_view, name='user-profile'),
    path('profile/edit/', CustomUserEditView.as_view(), name='edit-profile'),
    path('logout/', custom_logout, name='logout'),
    path('management/', include([
        path('', view_all_profile, name='all-profiles'),
        path('profile/<int:pk>/', view_profile, name='view-profile'),
        path('del-profile/<int:pk>/', delete_profile, name='delete-profile'),
    ])),
]
