from django.urls import path

from comments import views

urlpatterns = [
    path('articles/<str:slug>/comments', views.CommentView.as_view(), name='comment-article'),
    path('articles/<str:slug>/comments/<int:id>', views.DeleteCommentView.as_view(), name='comment-delete'),
]