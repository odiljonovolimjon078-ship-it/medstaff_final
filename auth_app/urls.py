from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('send-sms/', views.send_sms_code, name='send_sms'),
    path('verify-sms/', views.verify_sms_code, name='verify_sms'),
    path('profile/', views.profile_view, name='profile'),
]
