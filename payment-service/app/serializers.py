from rest_framework import serializers
from . models import Tenants


class PaymentSerializer(serializers.ModelSerializer):
    """
    name , subscription , subdomain , id
    """
    class Meta:
        model = Tenants
        fields = ['name', 'subscription_plan', 'subdomain', 'id']
        read_only_fields = ['id']
