from rest_framework import serializers
from app.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'contentType' , "contentId", 'parent', 'content', 'created_at']
