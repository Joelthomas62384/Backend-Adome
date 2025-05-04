from rest_framework import serializers
from  app.models import *




class CommunitySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()
    class Meta:
        model = Community
        fields = '__all__'


class CommunityChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunityChats
        fields = '__all__'


    def get_full_name(self, obj):
        return obj.user.user.full_name if obj.user and obj.user.user else None

    def get_profile_pic(self, obj):
        return obj.user.user.profile_pic if obj.user and obj.user.user else None


