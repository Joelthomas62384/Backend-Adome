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
                    'bank_ifsc_code': bank_ifsc_code,
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