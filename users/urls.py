from django.urls import path
from .views import UserLoginView, UserLogoutView, UserRegisterView, UserProfileDetailView, UserProfileUpdateView # , UserPasswordChangeView, CustomPasswordResetView, CustomPasswordResetDoneView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit'),
    # path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    # path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]