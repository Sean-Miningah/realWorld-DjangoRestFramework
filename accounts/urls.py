from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts import views 


# router = DefaultRouter()
# router.register('', views.UserView, basename="account-login")
# router.register('', views.account_registration, basename="account-registration")

urlpatterns = [
    path('users/login', views.account_login, name='account-login'),
    path('users/registration', views.account_registration, name="account-registration"),
    path('user', views.UserView.as_view(), name='user-account'),
]