from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts import views 

profile_router = DefaultRouter(trailing_slash=False)
profile_router.register('profiles', views.ProfileDetailView)


urlpatterns = [
    path('users/login', views.account_login, name='account-login'),
    path('users', views.account_registration, name="account-registration"),
    path('user', views.UserView.as_view(), name='user-account'),
    path('', include(profile_router.urls))
]