from django.urls import path, include 
from rest_framework.routers import DefaultRouter

from articles import views 

article_router = DefaultRouter(trailing_slash=False)
article_router.register('articles', views.ArticleView, basename='articles')
article_router.register('tags', views.TagView)

urlpatterns = [
    path('', include(article_router.urls))
]