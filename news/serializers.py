from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import *


class NewsSerializer(serializers.ModelSerializer):
    get_status = serializers.ReadOnlyField()

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ('author', )


class CommentSerializer(serializers.ModelSerializer):
    get_status = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'news')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class NewStatusSerializer(serializers.ModelSerializer):
    post_username = serializers.ReadOnlyField()
    get_likes = serializers.ReadOnlyField()
    get_dislikes = serializers.ReadOnlyField()

    class Meta:
        model = NewsStatus
        fields = '__all__'
        read_only_fields = ['author', ]


class CommentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentStatus
        fields = '__all__'
