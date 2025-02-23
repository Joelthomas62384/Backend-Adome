from app.models import LogoImages , UserCache
from rest_framework import serializers





class LogoImagesSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(use_url=True)
    """
    logo , created_at , user
    """
    class Meta:
        model = LogoImages
        fields = ['file', 'created_at',  'id']
        read_only_fields = ['created_at' , 'id']

