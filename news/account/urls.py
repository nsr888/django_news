from django.urls import path
from .views import user_login, user_logout, RegisterView

urlpatterns = [
    path('', user_login, name='acc'),
    path('logout/', user_logout, name='acc_logout'),
    path('register/', RegisterView.as_view(), name='registration'),
]
