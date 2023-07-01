import django_filters 

from articles.models import Article


class ArticleFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(method='tag_filter')
    author = django_filters.CharFilter(method='author_filter')
    favorited = django_filters.CharFilter(
        field_name='favorites', 
        method='is_favorited_filter', 
        label='Are they favorited')
    limit = django_filters.NumberFilter(method='limit_filter')
    offset = django_filters.NumberFilter(method='offset_filter')
    
    class Meta:
        model = Article
        fields = ['tag', 'author', 'favorited', 'limit', 'offset']
     
    def tag_filter(self, queryset, field_name, value):
        return queryset.filter(tags__name__in=[value])
    
    def author_filter(self, queryset, field_name, value):
        return queryset.filter(author__username__icontains=value)
    # filter by articles that have been favorited by the user name passed   
    def is_favorited_filter(self, queryset, field_name, value):
        return queryset.filter(favorites__username__icontains=value)
    
    # Limit number of articles (default is 20):
    def limit_filter(self, queryset, field_name, value):
        return queryset[:value]
    
    # Offset/skip number of articles (default is 0):
    def offset_filter(self, queryset, field_name, value):
        return queryset[value:]