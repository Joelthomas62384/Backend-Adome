from rest_framework import serializers
from app.models import TenantPayments



class TenantPaymentSerializer(serializers.ModelSerializer):
    """
    tenant = models.OneToOneField(Tenants , on_delete=models.CASCADE)
    razorpay_account_id = models.CharField(max_length=100 , null=True , blank=True)
    email = models.EmailField(null=True , blank=True,max_length=100)
    name = models.CharField(max_length=255,blank=True)
    bank_account_number = models.CharField(max_length=100 , null=True , blank=True)
    bank_ifsc = models.CharField(max_length=100 , null=True , blank=True)

    def __str__(self):
        return self.tenant.name
    
    """
    class Meta:
        model = TenantPayments
        fields = "__all__"
        read_only_fields = ['id','tenant']