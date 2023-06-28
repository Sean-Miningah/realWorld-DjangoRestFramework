from django.http import Http404
from rest_framework import viewsets , status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 

from articles.models import Article
from articles.serializers import ArticleSerializer

# Create your views here.
class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer 
    permission_classes=[IsAuthenticated]
    lookup_field='slug'
    
    
    def create(self, request, *args, **kwargs):
        article_data = request.data.get('article')
        serializer = self.get_serializer(data=article_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"article":serializer.data}, headers=headers)
    