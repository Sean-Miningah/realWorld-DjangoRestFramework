from django.urls import path, include 
from rest_framework.routers import DefaultRouter

from articles import views 

article_router = DefaultRouter(trailing_slash=False)
article_router.register('article', views.ArticleView)

urlpatterns = [
    path('', include(article_router.urls))
]