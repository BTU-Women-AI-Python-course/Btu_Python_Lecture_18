from django.urls import path

from user.views import register, home, login, logout, CustomAuthToken

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('api/token/', CustomAuthToken.as_view(), name='token_obtain')
]