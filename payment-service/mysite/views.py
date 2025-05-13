from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app.models import *
from .serializers import *
import razorpay
from django.conf import settings
from razorpay.errors import BadRequestError, ServerError
from app.serializers import OrderSerializer
from app.producers import Publisher
from django.db import transaction
from django.db.models.aggregates import Sum
from django.db.models.functions import TruncMonth , TruncDate
from django.utils import timezone
from dateutil.relativedelta import relativedelta




razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class PaymentGatewayRegister(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        name = data.get('name')
        phone = data.get('phone')
        bank_account_number = data.get('bank_account_number')
        bank_ifsc_code = data.get('bank_ifsc')
        pan_number = data.get('pan_number')

        if not all([email, name, phone, bank_account_number, bank_ifsc_code, pan_number]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            encrypted_email = TenantPayments().encrypt_value(email)

            tenant_payment, created = TenantPayments.objects.update_or_create(
                tenant=request.tenant,
                defaults={
                    'email': email,
                    'name': name,
                    'phone': phone,
                    'bank_account_number': bank_account_number,
                    'bank_ifsc': bank_ifsc_code,
                    'pan_number': pan_number,
                    'encrypted_email': encrypted_email,
                }
            )

            return Response({
                'message': 'Tenant payment details saved successfully.',
                'created': created,
                'data': {
                    'email': email,
                    'name': name,
                    'phone': phone,
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# user_id = models.CharField(max_length=100)
#     course = models.ForeignKey(CourseCache, on_delete=models.CASCADE)
#     tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE , null=True , blank=True)
#     course_title = models.CharField(max_length=255)
#     order_product = models.CharField(max_length=100)
#     order_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.CharField(max_length=10, default="INR")
#     razorpay_order_id = models.CharField(max_length=100, unique=True)
#     order_payment_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
#     order_signature = models.CharField(max_length=256, blank=True, null=True)
#     is_paid = models.BooleanField(default=False)
#     is_verified = models.BooleanField(default=False)
#     order_status = models.CharField(max_length=20, default="created")
#     payment_method = models.CharField(max_length=50, blank=True, null=True)
#     payment_time = models.DateTimeField(blank=True, null=True)
#     order_date = models.DateTimeField(auto_now_add=True)

class CreateCourseOrderView(APIView):
    def post(self ,request):
        data = request.data
        course_id = data.get("course_id")
        course = CourseCache.objects.get(id=course_id)
        amount = course.price

        if not all([course_id , amount]):
            return Response({"error": "Missing fields"}, status=400)
        currency = 'INR'
        amount_paise = int(float(amount) * 100)
        razorpay_order = razorpay_client.order.create({
            "amount" : amount_paise,
            "currency" :currency,
            "payment_capture" : 1,
            "notes" : {
                "course_id" : course_id
            }
        })
        razorpay_order_id=razorpay_order["id"]
        order = Order.objects.create(
            razorpay_order_id=razorpay_order_id,
            order_amount = amount,
            user = request.tenantuser,
            course = course,
            tenant = request.tenant,
            order_product = "course",
            currency = currency,
        )
        return Response({
            'razorpay_order_id': razorpay_order_id,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_amount': amount_paise,
        'currency': currency,
        'order_id': order.id
        })
    
    


class VerifyPayment(APIView):
    @transaction.atomic
    def post(self ,request):
        data = request.data

        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")

        try : 
            razorpay_client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature

            })
            order = Order.objects.get(razorpay_order_id=razorpay_order_id) 
            
            order.is_paid = True
            order.order_payment_id = razorpay_payment_id
            order.order_signature = razorpay_signature
            order.save()
            serializer = OrderSerializer(order)
            Publisher(serializer.data , 'order' , 'created')

            wallet = TenantWallet.objects.get(tenant=request.tenant)
            wallet.total_amount +=order.order_amount
            wallet.save()
            return Response({
                "success": True,
                "message": "Payment verified and order updated successfully.",
                "order_id": order.id,
                "payment_id": razorpay_payment_id,
            })
        

        except razorpay.errors.SignatureVerificationError:
            return Response({"success": False, "error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)
        


from datetime import timedelta , datetime
class WalletDetailsInAnalytics(APIView):

    """
    
class TenantWallet(models.Model):
    tenant = models.OneToOneField(Tenants , on_delete=models.CASCADE)
    total_amount = models.DecimalField(default=0 , decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.tenant.name
    



class Order(models.Model):
    user = models.ForeignKey(TenantUsers , on_delete=models.CASCADE , null=True ,blank=True)
    course = models.ForeignKey(CourseCache, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenants, on_delete=models.CASCADE , null=True , blank=True)
    course_title = models.CharField(max_length=255)
    order_product = models.CharField(max_length=100)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    order_payment_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    order_signature = models.CharField(max_length=256, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20, default="created")
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_time = models.DateTimeField(blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True)

    """
    def get(self ,request):
        wallet = TenantWallet.objects.get(tenant=request.tenant)
        seven_days_ago = timezone.now() - timedelta(days=7)
        seven_days_after_total = (
            Order.objects
            .filter(tenant=request.tenant , order_date__gte=seven_days_ago , is_paid=True)
            .aggregate(total_amount=Sum('order_amount'))
        )['total_amount'] or 0
        serializer = TenantWallentAnalytics({"total_amount" : wallet.total_amount , "withdrawal_amount" : wallet.total_amount-seven_days_after_total})
        return Response(serializer.data , status=200)



class TotalOrdersWeGotInSixMonths(APIView):
    def get(self, request):
        today = timezone.now().replace(day=1) 
        six_months = [today - relativedelta(months=i) for i in reversed(range(6))]

        queryset = (
            Order.objects.filter(is_paid=True, order_date__gte=six_months[0])
            .annotate(month=TruncMonth("order_date"))
            .values("month")
            .annotate(total_amount=Sum("order_amount"))
        )

        amount_by_month = {
            item["month"].strftime("%b %Y"): float(item["total_amount"] or 0)
            for item in queryset
        }

        # Build complete 6-month data
        final_data = []
        for date in six_months:
            label = date.strftime("%b %Y")
            total = amount_by_month.get(label, 0)
            final_data.append({"month": label, "total_amount": total})

        serializer = MonthlyOrderSummarySerializer(final_data, many=True)
        return Response(serializer.data)




class TotalOrdersWeGotInSevenDays(APIView):
    def get(self, request):
        today = timezone.now().date()
        start_date = today - timedelta(days=6)
        date_range = [start_date + timedelta(days=i) for i in range(7)]

        queryset = (
            Order.objects.filter(is_paid=True, order_date__date__gte=start_date)
            .annotate(date=TruncDate("order_date"))
            .values("date")
            .annotate(total_amount=Sum("order_amount"))
        )

        amount_by_date = {
            item["date"]: float(item["total_amount"] or 0)
            for item in queryset
        }

        final_data = [
            {
                "date": date.strftime("%a %d %b"),
                "total_amount": amount_by_date.get(date, 0)
            }
            for date in date_range
        ]

        serializer = DailyOrderSummarySerializer(final_data, many=True)
        return Response(serializer.data)
    


class PreviousOrderLogs(APIView):
    def get(self ,request):
        order = Order.objects.filter(tenant=request.tenant, is_paid=True).order_by('-id')[:12]
        serializer= OrderAnalyticSerializer(order, many=True)
        print(serializer.data)
        return Response(serializer.data , status=200)
    


class CheckConnectedPayment(APIView):
    def get(self, request):
        tenant_payment = TenantPayments.objects.filter(tenant=request.tenant)
        serializer = CheckPaymentConnect({"connected" : tenant_payment.exists})
        return Response(serializer.data , status=200)


