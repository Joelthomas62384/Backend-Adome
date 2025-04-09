from rest_framework import serializers
from app.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'contentType' , "contentId", 'parent', 'content', 'created_at']
        read_only_fields = ['user']

    def get_user(self, obj):
        return {
            "full_name":obj.user.user.full_name,
            "profile_pic":obj.user.user.profile_pic,
            
        }
