from rest_framework import serializers
from . models import *




class TenantSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Tenants
        fields = [

           'id' ,'name', 'domain', 'contact_email', 'founding_year',
            'location', 'description', 'blog', 'community', 'newsletter'  , 'admin' , 'subscription_plan' , 'subdomain'
        ]
        read_only_fields = ['id']
        