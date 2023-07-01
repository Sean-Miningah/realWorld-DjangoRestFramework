from django.http import Http404
from rest_framework import viewsets , status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response 
from django.db.models import Q

from accounts.models import User
from articles.models import Article
from articles.serializers import ArticleSerializer
from articles.filters import ArticleFilter

# Create your views here.
class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer 
    permission_classes=[IsAuthenticated]
    lookup_field='slug'
    filterset_class = ArticleFilter
    
    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticatedOrReadOnly()]

        return super().get_permissions()
    
    
    def create(self, request, *args, **kwargs):
        try:
            article_data = request.data.get('article')
            serializer = self.get_serializer(data=article_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"article":serializer.data}, headers=headers)
        
        except Exception:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)   
            
    @action(detail=True, methods=['post'])
    def favorite(self, request, slug, *args, **kwargs):
        try:
            article = Article.objects.filter(slug=slug)[0]
            
            if not article.favorites.filter(id=request.user.id).exists():
                article.favorites.add(request.user)
                serializer = self.get_serializer(article)
                return Response({"article": serializer.data})
            
            else:
                return  Response({"errors": {
                    "body": [
                        "Already Favourited Article"
                    ]
                }})   
        except Exception:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)  
            
        
            
    @action(detail=False)
    def feed(self, request, *args, **kwargs):
        try:
            followed_authors = User.objects.filter(followers=request.user)
            queryset = self.get_queryset()
            articles = queryset.filter(
                author__in=followed_authors).order_by('-created')
            queryset = self.filter_queryset(articles)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({"articles": serializer.data})
               
        except Exception:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)   
             
        
    def retrieve(self, request, slug, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            article = queryset.get(slug=slug)
            print(article.title)
            serializer = self.get_serializer(article)
            
            return Response({"article": serializer.data})
            
        except Exception:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)
            
        
    
    def update(self, request, slug, *args, **kwargs):
        
        try:
            queryset = self.get_queryset()
            article = queryset.get(slug=slug)
            
            if request.user != article.author:
                return Response({"errors": {
                    "body": [
                        "UnAuthorized Action"
                    ]
                }}, status=status.HTTP_401_UNAUTHORIZED)
                
            request_data = request.data.get('article')
            serializer = self.get_serializer(article, data=request_data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response({"article": serializer.data})
        
        except Exception:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)
            
        
    
    def destroy(self, request, slug, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            article = queryset.get(slug=slug)
        
            if request.user != article.author:
                return Response({"errors": {
                    "body": [
                        "UnAuthorized Action"
                    ]
                }}, status=status.HTTP_401_UNAUTHORIZED)
                
            article.delete()
            return Response(status=status.HTTP_200_OK)
          
        except Exception:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)
            
