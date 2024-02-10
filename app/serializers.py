from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from app.models import Post, Rating


class PostSerializer(ModelSerializer):
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('title', 'content', 'rating_avg', 'rating_count', 'user_rating',)

    def get_user_rating(self, obj):
        """
        Returns the authenticated user's rating for the Post instance,
        or None if the user is not authenticated or has not rated the post.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_rating = Rating.objects.filter(owner=request.user, post=obj).values('rate').first()
            return user_rating['rate'] if user_rating else None
        return None


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
