from rest_framework import serializers
from . models import User





class UserSerializer(serializers.ModelSerializer):
    """
    
   
   id name , email , full_name , username , profile_pic , is_staff , is_active , is_superuser , created_at , updated_at
    """
    class Meta:
        model = User
        fields = ['name', 'id' ,'email', 'full_name', 'username', 'profile_pic', 'is_staff', 'is_active', 'is_superuser', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at' , 'id']


class TenantUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    tenant = serializers.PrimaryKeyRelatedField(read_only=True)
    """
    
    tenant , user , is_admin , is_staff , blocked , banned , created_at
    """
    class Meta:

        
        model = User
        fields = ['tenant', 'user', 'is_admin', 'is_staff', 'blocked', 'banned', 'created_at']
        read_only_fields = ['created_at']

