from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from taggit.models import Tag

from accounts.models import User
from articles.models import Article
from articles.serializers import ArticleSerializer, TagSerializer
from articles.filters import ArticleFilter


class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    filterset_class = ArticleFilter
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            article_data = request.data.get('article')
            serializer = self.get_serializer(data=article_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"article": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            # FIXME: The status code should be 400 for Bad Request, not 404
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, slug, *args, **kwargs):
        try:
            article = Article.objects.get(slug=slug)

            if request.method == 'POST':
                if article.favorites.filter(id=request.user.id).exists():
                    return Response({"errors": {
                        "body": [
                            "Already Favorited Article"
                        ]
                    }})
                article.favorites.add(request.user)

            elif request.method == 'DELETE':
                if not article.favorites.filter(id=request.user.id).exists():
                    # FIXME: Raising Exception directly is not a good practice, should use a more specific exception
                    raise Exception("Article not favorited by user")
                article.favorites.remove(request.user.id)

            serializer = self.get_serializer(article)
            return Response({"article": serializer.data})

        except Article.DoesNotExist:
            return Response({"errors": {
                "body": [
                    "Article not found"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_400_BAD_REQUEST)  # FIXME: Should return 400 Bad Request, not 404

    @action(detail=False)
    def feed(self, request, *args, **kwargs):
        try:
            followed_authors = User.objects.filter(followers=request.user)
            articles = self.get_queryset().filter(
                author__in=followed_authors).order_by('-created')
            articles = self.filter_queryset(articles)

            serializer = self.get_serializer(articles, many=True)
            response = {
                'articles': serializer.data,  # FIXME: Key should be 'articles', not 'comments'
                'articleCount': len(serializer.data)
            }
            return Response(response)

        except Exception as e:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_400_BAD_REQUEST)  # FIXME: Should return 400 Bad Request, not 404

    def retrieve(self, request, slug, *args, **kwargs):
        try:
            article = self.get_queryset().get(slug=slug)
            serializer = self.get_serializer(article)
            return Response({"article": serializer.data})

        except Article.DoesNotExist:
            return Response({"errors": {
                "body": [
                    "Article not found"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_400_BAD_REQUEST)  # FIXME: Should return 400 Bad Request, not 404

    def update(self, request, slug, *args, **kwargs):
        try:
            article = self.get_queryset().get(slug=slug)

            if request.user != article.author:
                return Response({"errors": {
                    "body": [
                        "Unauthorized Action"
                    ]
                }}, status=status.HTTP_403_FORBIDDEN)  # FIXME: Should return 403 Forbidden, not 401 Unauthorized

            request_data = request.data.get('article')
            serializer = self.get_serializer(article, data=request_data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({"article": serializer.data})

        except Article.DoesNotExist:
            return Response({"errors": {
                "body": [
                    "Article not found"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_400_BAD_REQUEST)  # FIXME: Should return 400 Bad Request, not 404

    def destroy(self, request, slug, *args, **kwargs):
        try:
            article = self.get_queryset().get(slug=slug)

            if request.user != article.author:
                return Response({"errors": {
                    "body": [
                        "Unauthorized Action"
                    ]
                }}, status=status.HTTP_403_FORBIDDEN)  # FIXME: Should return 403 Forbidden, not 401 Unauthorized

            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # FIXME: Should return 204 No Content, not 200 OK

        except Article.DoesNotExist:
            return Response({"errors": {
                "body": [
                    "Article not found"
                ]
            }}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_400_BAD_REQUEST)  # FIXME: Should return 400 Bad Request, not 404


class TagView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            tags = [element.name for element in queryset]
            serializer = self.get_serializer({'tags': tags})
            return Response(serializer.data)

        except Exception as e:
            return Response({"errors": {
                "body": [
                    "Bad Request"
                ]
            }}, status=status.HTTP_400_BAD_REQUEST)  # FIXME: Should return 400 Bad Request, not 404
