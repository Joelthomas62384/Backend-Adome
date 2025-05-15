from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app.models import *
from .serializers import *
import razorpay
from django.conf import settings



client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class SubscriptionCreateView(APIView):
    def post(self ,request):
        data = request.data
        plan_type = data.get('plan_type')

        if plan_type == "1":
            subscription , created = Subscription.objects.get_or_create(tenant=request.tenant)
            subscription.plan = '1'
            subscription.razorpay_subscription_id = None
            subscription.status = 'active'
            subscription.billing_cycle_end = None
            subscription.grace_period_end = None
            subscription.save()
            serializer = SubscriptionSerializer({'plan' : 'Free','message': 'Free plan activated' })
        
            return Response(serializer.data , status=200)
        if plan_type == '2':
            plan_id = "plan_PwPYE1xi2I2KdG"
            try:
                subscription_data = {
                    'plan_id' :plan_id,
                    'total_count' : 12,
                    'customer_notify':1
                }
                razorpay_subscription = client.subscription.create(subscription_data)
            
                subscription, created = Subscription.objects.get_or_create(tenant=request.tenant)

                subscription.plan = '2'
                subscription.razorpay_subscription_id = razorpay_subscription['id']
                subscription.status = 'created'
                subscription.billing_cycle_end = datetime.now() + timedelta(days=30)  
                subscription.save()
                serializer = SubscriptionSerializer({'plan' : 'Premium','message': 'Premium plan activated','subscription_id': razorpay_subscription['id'],'razorpay_key': settings.RAZORPAY_KEY_ID, })
                # response_data = {
                #     'status': 'success',
                #     'subscription_id': razorpay_subscription['id'],
                #     'razorpay_key': settings.RAZORPAY_KEY_ID,
                #     'plan': 'PREMIUM'
                # }
                
                return Response(serializer.data , status=200)
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)}, status=400)


            

class VerifyPayment(APIView):
    def post(self,request):
        data = request.data
        try:
            client.utility.verify_payment_signature({
                'razorpay_subscription_id': data['razorpay_subscription_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })
            
            subscription = Subscription.objects.get(razorpay_subscription_id=data['razorpay_subscription_id'])
            subscription.status = 'active'
            subscription.billing_cycle_end = datetime.now() + timedelta(days=30)  
            subscription.save()
            serializer = SuccessSerializer({'message' : "Payment verified and subscription activated"})
            # Publisher({'plan' : '2' , 'tenant' : request.tenant.id} , 'subscription' , 'updated')
            return Response(serializer.data,status=200)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)
        


class CancelPayment(APIView):
    def post(self , request):
        try:
            subscription = Subscription.objects.get(tenant= request.tenant ,plan='2' ,status__in=['active' , 'grace'])
            client.subscription.cancel(subscription.razorpay_subscription_id)
            subscription.status='cancelled'
            subscription.save()
            serializer = SuccessSerializer({'message' : f'Subscription cancelled. Premium access remains until {subscription.billing_cycle_end.strftime("%Y-%m-%d")}.'})
            return Response(serializer.data , status=200)
        except Subscription.DoesNotExist:
            serializer = SuccessSerializer({'message' : 'No active premium subscription found.'})
            return Response(serializer.data ,status=400)
        except Exception as e:
            serializer = SuccessSerializer({'message': f'Error cancelling subscription: {str(e)}'})
            return Response(serializer.data ,status=400)

