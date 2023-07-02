from rest_framework import serializers 
from accounts.models import User 


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'bio', 'image')
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'password':
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance   
    


class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    
    class Meta:
        model = User 
        fields = ('username', 'bio', 'image', 'following')
    
    def get_following(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.followers.filter(pk=user.id).exists()
        return False