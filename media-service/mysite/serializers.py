from app.models import LogoImages , UserCache, TenantImageBucket
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


class TenantImageBucketSerializer(serializers.ModelSerializer):

    """
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tenant_images/')
    content_type = models.CharField(max_length=50)
    user = models.ForeignKey(UserCache, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    """

    class Meta:
        model = TenantImageBucket
        fields = [ 'image', 'id' ,'content_type']
        read_only_fields = ['id']
