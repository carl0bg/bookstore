from django.urls import path
from users.views import login, profile, logout, UserRegistrationView, register_confirm #,EmailVerificationView
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', login, name = 'login'),
    # path('registration/', registration, name = 'registration'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/', login_required(profile.as_view()), name = 'profile'),
    path('logout/', logout, name = 'logout'),
    path("register_confirm/<token>/", register_confirm, name="register_confirm"),
    # path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
