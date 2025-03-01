from rest_framework import serializers
from . models import *




class TenantSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Tenants
        fields = [

           'id' ,'name', 'domain', 'contact_email', 
            'location', 'description', 'blog', 'community', 'newsletter'  , 'admin' , 'subscription_plan' , 'courses', 'subdomain' , 'contact_email' , 'logo'
        ]
        read_only_fields = ['id']
    def create(self, validated_data):
        validated_data['admin'] = self.context['request'].user 
        return super().create(validated_data)

        # '/media/logos/brototype_logo_vuloeXg.png'