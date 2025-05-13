from rest_framework import serializers
from app.models import TenantPayments , Order



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


    


class TenantWallentAnalytics(serializers.Serializer):
    total_amount = serializers.IntegerField(read_only=True)
    withdrawal_amount = serializers.IntegerField(read_only=True)




class MonthlyOrderSummarySerializer(serializers.Serializer):
    month = serializers.CharField()
    total_amount = serializers.FloatField()


class DailyOrderSummarySerializer(serializers.Serializer):
    date = serializers.CharField()
    total_amount = serializers.FloatField()



class OrderAnalyticSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    course = serializers.SerializerMethodField(read_only=True)
    profile_pic = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['user' , 'id' , 'order_amount' , 'course' ,'order_date' , 'profile_pic']

    def get_user(self , obj):
        try:
            return obj.user.user.full_name
        except:
            return None
    def get_profile_pic(self , obj):
            try:
                return obj.user.user.profile_pic
            except:
                return None


    def get_course(self, obj):
        try:
            return obj.course.title
        except :
            return None
        
    

class CheckPaymentConnect(serializers.Serializer):
    connected = serializers.BooleanField()