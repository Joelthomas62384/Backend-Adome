from rest_framework import serializers
from . models import User , TenantUsers





class UserSerializer(serializers.ModelSerializer):
    """
    
   
   id name , email , full_name , username , profile_pic , is_staff , is_active , is_superuser , created_at , updated_at
    """
    class Meta:
        model = User
        fields = [ 'id' ,'email', 'full_name', 'username', 'profile_pic', 'is_staff', 'is_active', 'is_superuser', 'created_at', 'updated_at']
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


class TenantUsersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = TenantUsers
        fields = ['tenant', 'user', 'is_admin', 'is_staff', 'blocked', 'banned', 'created_at' , 'id' ,'designation']
        read_only_fields = ['created_at']

    
    
    def get_designation(self, obj):
        tenant = self.context.get('request').tenant
        tenant_user = TenantUsers.objects.get(user=obj , tenant=tenant)
        if tenant_user:
            return tenant_user.designation
        return None
            
class UserSerializerNew(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [  'email', 'full_name', 'username', 'profile_pic']

class TenantUsersSerializer(serializers.ModelSerializer):
    user = UserSerializerNew(read_only=True)
    role = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = TenantUsers
        fields = ['tenant', 'user', 'role', 'blocked',  'banned', 'created_at' , 'id' ,'designation' , 'is_admin' , 'is_staff', 
                  'hasStaffPermission', 'hasBlogPermission' , 'hasCommunityPermission' , "hasNewsletterPermission","hasCoursesPermission" , "hasBuilderPermission"]
        read_only_fields = ['created_at']

    def get_role(self, obj):
        tenant_user = obj
        if tenant_user:
            if tenant_user.is_admin:
                return "admin"
            elif tenant_user.is_staff:
                return "staff"  
            else:
                return "user"
        return None

class TotalUserSerializer(serializers.Serializer):
    total_users  = serializers.IntegerField()




class UserAnalyticsSerializer(serializers.Serializer):
    month = serializers.DateTimeField()
    joined = serializers.IntegerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        formatted_month = instance['month'].strftime("%b %Y")
        return {
            "month": formatted_month,
            "joined": data["joined"],
        }
    
class TenantUserAnalyticsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = TenantUsers
        fields = ['user' , 'profile_pic','created_at' , 'id']
    
    def get_user(self , obj):
        try:
            return obj.user.full_name
        except :
            return None
        
    def get_profile_pic(self, obj):
        try:
            return obj.user.profile_pic
        except :
            return None
