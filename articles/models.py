import markdown
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model 
from django.contrib.auth.models import AnonymousUser
from django.utils.text import slugify
from django.urls import reverse


User = get_user_model()

class ArticleQuerySet(models.QuerySet):
    def with_favorites(self, user: AnonymousUser | User) -> models.QuerySet:

        return self.annotate(
            num_favorites=models.Count("favorites"),
            # true if user is authenticated 
            is_favorite=models.Exists(
                get_user_model().objects.filter(
                    pk=user.id, favorites=models.OuterRef("pk")
                ),
            )
            if user.is_authenticated
            else models.Value(False, output_field=models.BooleanField()),
        )


ArticleManager = models.Manager.from_queryset(ArticleQuerySet)

class Article(models.Model):
    author =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    tags = TaggableManager(blank=True)
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="favorites"
    )
    slug = models.SlugField(unique=True, max_length=255)

    
    objects = ArticleManager()
    
    # @property
    # def slug(self) -> str:
    #     return slugify(self.title)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self) -> str:
        return reverse(
            "article_detail",
            kwargs={
                "article_id": self.id,
                "slug": self.slug,
            }
        )
        
    def as_markdown(self) -> str:
        return markdown.markdown(self.content, safe_mode="escape", extensions=["extra"])