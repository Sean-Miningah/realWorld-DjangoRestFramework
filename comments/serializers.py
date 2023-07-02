from rest_framework import serializers

from comments.models import Comment
from articles.serializers import AuthorSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created', format='%Y-%m-%dT%H:%M:%S.%fZ', required=False)
    updatedAt = serializers.DateTimeField(source='updated', format='%Y-%m-%dT%H:%M:%S.%fZ', required=False)
    body = serializers.CharField(source='content', required=True)
    
    
    class Meta:
        model = Comment 
        fields = ['id', 'createdAt', 'updatedAt', 'body', 'author']
        
    
    def get_author(self, obj):
        request = self.context.get('request')
        serializer = AuthorSerializer(obj.author, context={'request': request})
        return serializer.data
    
    def create(self, validated_data):
        comment = Comment(
            **validated_data,
            author=self.context['request'].user, 
            article=self.context['article']
        )
        comment.save()
        return comment