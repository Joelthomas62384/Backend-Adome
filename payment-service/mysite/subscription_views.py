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




class SubscriptionCreateView(APIView):
    def post(self ,request):
        data = request.data
        plan_type = data.get('plan_type')

        if plan_type == "1":
            subscription , created = Subscription.objects.get_or_create(tenant=request.tenant)
            subscription.plan = 'FREE'
            subscription.razorpay_subscription_id = None
            subscription.status = 'active'
            subscription.billing_cycle_end = None
            subscription.grace_period_end = None
            subscription.save()
        
            return Response(status=200)
            
