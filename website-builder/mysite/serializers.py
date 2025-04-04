from rest_framework import serializers
from app.models import *



class WebsiteSerialzer(serializers.ModelSerializer):
    

    class Meta:
        model = Website
        fields = ('id', 'tenant', 'web_data', 'created_at', 'updated_at' , 'title' , 'is_default' , 'live_mode')
        read_only_fields = ['created_at', 'updated_at' , 'id' , 'tenant']


