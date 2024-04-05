from django.urls import path
from users.views import login, registration, profile, logout
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', login, name = 'login'),
    path('registration/', registration, name = 'registration'),
    path('profile/', login_required(profile.as_view()), name = 'profile'),
    path('logout/', logout, name = 'logout'),
]
