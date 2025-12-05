from django.urls import path
from .views import login_view, refresh_token, register_view, UserProfileView, UserUpdateView

urlpatterns = [
    path('login/', login_view, name = 'login'),
    path('refresh/', refresh_token, name = 'refresh'),
    path('register/', register_view, name = 'register'),
    path('profile/', UserProfileView.as_view(), name = 'profile'),
    path('profile/update/', UserUpdateView.as_view(), name='profile_update')
]
