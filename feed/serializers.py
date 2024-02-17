from rest_framework import serializers

from currency_converter.models import ConversionHistory, CurrencyConversion
from feed.models import Post, Comment, FeedUser


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'message', 'post']


class FeedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedUser
        fields = ['id', 'name']
