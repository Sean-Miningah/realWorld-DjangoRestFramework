from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import  AccessToken

from articles.models import Article


User = get_user_model() 


class ArticleViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', email='test@email@test', password='testpassword'
            )
        self.access_token = str(AccessToken.for_user(self.user))
        
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.access_token
        )
        self.article_data = {
            "article": {
                "title": "How dragon",
                "description": "Ever wonder how?",
                "body": "You have to believe",
                "tagList": ["rs", "ans", "dragons"]
            }
        }
        
        self.article_create_data = {
            'author': self.user, 
            'title' :'Old Title', 
            'summary' : 'Old summary',
            'content' : 'Old content',
            'slug' : 'test-slug'
        }
    
    def test_get_articles(self):
        url = '/api/articles'
        
        new_client = APIClient()
        response = new_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_article_feed(self):
        url = '/api/articles/feed'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_article(self):
        url = '/api/articles'
        response = self.client.post(url, data=self.article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_article(self):
        article = Article.objects.create(
            **self.article_create_data
        )
        url = f'/api/articles/{article.slug}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_update_article(self):
        article = Article.objects.create(
            **self.article_create_data
            )
        url = f'/api/articles/{article.slug}'
        updated_article_data = {
            "article": {
                "slug": "how-to-train-your-dragon",
                "title": "Updating how to train you dragon",
                "description": "Ever wonder how dragon",
                "body": "Believe in being updated lower and lower",
                "tagList": [
                    "34-love"
                ]
            }
        }
        response = self.client.put(url, data=updated_article_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_delete_article(self):
        article = Article.objects.create(
            author=self.user, title='Old Title', summary='Old summary', content='Old content', slug='test-slug'
            )
        url = f'/api/articles/{article.slug}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    def test_favorite_article(self):
        article = Article.objects.create(**self.article_create_data)
        url = f'/api/articles/{article.slug}/favorite'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_unfavorite_article(self):
        article = Article.objects.create(**self.article_create_data)
        article.favorites.add(self.user)
        url = f'/api/articles/{article.slug}/favorite'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class TagViewSet(APITestCase):

    def test_list_tags(self):
        url = '/api/tags'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)