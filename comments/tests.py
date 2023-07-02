from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import  AccessToken

from articles.models import Article
from comments.models import Comment


User = get_user_model()


class CommentViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test@email.email')
        
        self.access_token = str(AccessToken.for_user(self.user))
        
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        
        self.new_article_data = {
            'author': self.user, 
            'title' :'Old Title', 
            'summary' : 'Old summary',
            'content' : 'Old content',
            'slug' : 'test-slug'
        }
        self.article = Article.objects.create(
            **self.new_article_data)
        

    def test_get_comments_list(self):
        url = f'/api/articles/{self.article.slug}/comments'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)      
        
    def test_create_comment(self):
        url = f'/api/articles/{self.article.slug}/comments'
        data = {'comment': {'body': 'This is a test comment'}}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class DeleteCommentViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='email@email.email'
            )
        self.article = Article.objects.create(
            title='Test Article', summary='test-summary', content='test-content', author=self.user
            )
        self.comment = Comment.objects.create(
            article=self.article, author=self.user, content='Test comment')

    def test_delete_comment(self):
        url = f'/api/articles/{self.article.slug}/comments/{self.comment.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)