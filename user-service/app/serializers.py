from rest_framework import serializers
from . models import User , TenantUsers





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
    username = serializers.SerializerMethodField(read_only=True)
    """
    
    tenant , user , is_admin , is_staff , blocked , banned , created_at
    """
    class Meta:

        
        model = TenantUsers
        fields = ['tenant', 'user', 'is_admin', 'is_staff', 'blocked', 'banned', 'created_at' , 'id' ,'username']
        read_only_fields = ['created_at']

    def get_username(self,obj):
        return obj.user.username



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserTenantSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    designation = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["name" , "email" , "full_name" , "username" , "profile_pic" , "role" , "designation"]

    
    def get_role(self, obj):
        tenant = self.context.get('request').tenant
        tenant_user = TenantUsers.objects.get(user=obj , tenant=tenant)
        if tenant_user:
            if tenant.is_admin:
                return "admin"
            elif tenant.is_staff:
                return "staff"  
            else:
                return "user"
        return None
    def get_designation(self, obj):
        tenant = self.context.get('request').tenant
        tenant_user = TenantUsers.objects.get(user=obj , tenant=tenant)
        if tenant_user:
            return tenant_user.designation
        return None
            