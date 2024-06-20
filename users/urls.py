from django.urls import path
from .views import RegisterView, ProfileView, EditProfileView, LoginView, LogoutView

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='profile-update'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login')
]
