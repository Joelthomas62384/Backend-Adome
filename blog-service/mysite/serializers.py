from rest_framework import serializers
from app.models import Blog, UserCache

class BlogSerializer(serializers.ModelSerializer):
    """
    Blog Model:
    - user = ForeignKey(TenantUsers)
    - tenant = ForeignKey(Tenants)
    - title, image, content, published, timestamps
    """
    userDetails = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['id' ,  'tenant' ,'user', 'created_at' , 'updated_at' ,]

    def get_userDetails(self, obj):
        if obj.user and obj.user.user:
            user_cache = UserCache.objects.filter(id=obj.user.user.id).first()
            if user_cache:
                return {
                    'profile_pic': user_cache.profile_pic,
                    'full_name': user_cache.full_name
                }
        
        return {"profile_pic": None, "full_name": None}  

    