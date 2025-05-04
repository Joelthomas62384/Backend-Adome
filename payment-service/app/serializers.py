from rest_framework import serializers
from . models import Tenants, Order





class PaymentSerializer(serializers.ModelSerializer):
    """
    name , subscription , subdomain , id
    """
    class Meta:
        model = Tenants
        fields = ['name', 'subscription_plan', 'subdomain', 'id']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['course' , 'user' ,'tenant' , 'course_title']