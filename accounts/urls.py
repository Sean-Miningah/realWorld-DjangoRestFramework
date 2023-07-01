from django.urls import path 

from accounts import views 


urlpatterns = [
    path('users/login', views.account_login, name='account-login'),
    path('users', views.account_registration, name="account-registration"),
    path('user', views.UserView.as_view(), name='user-account'),
    path('profiles/<str:username>', views.ProfileDetailView.as_view({'get': 'list'}), name='profile'),
    path('profiles/<str:username>/follow', views.ProfileDetailView.as_view({'post': 'follow', 'delete': 'unfollow'}), name='follow-profile')
]