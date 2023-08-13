from django.urls import path
from .views import SignUp, UserProfile, signup_mail_view, SignUpConfirm

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('<int:pk>/profile/', UserProfile.as_view(), name='user_profile'),
    path('signup_mail_sent', signup_mail_view, name='signup_mail'),
    path('<int:pk>/confirm_signup', SignUpConfirm.as_view(), name='confirmation_signup'),
]