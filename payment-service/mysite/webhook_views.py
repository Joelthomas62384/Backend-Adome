
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from app.models import Subscription
import razorpay
from django.conf import settings
from datetime import datetime , timedelta
import json






client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



@csrf_exempt
def webhook(request):
    webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
    try:
        client.utility.verify_webhook_signature(
            request.body.decode('utf-8'),
            request.headers['X-Razorpay-Signature'],
            webhook_secret
        )
        event = json.loads(request.body)
        subscription_id = event['payload']['subscription']['entity']['id']
        subscription = Subscription.objects.get(razorpay_subscription_id=subscription_id)

        if event['event'] == 'subscription.authenticated':
            subscription.status = 'authenticated'
            subscription.save()
            # send_mail(
            #     'Payment Authorized',
            #     f'Dear {subscription.user.username},\nYour premium plan payment of ₹5000 has been authorized. Your subscription will be activated soon.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [subscription.user.email],
            #     fail_silently=False,
            # )

        elif event['event'] == 'subscription.activated':
            subscription.status = 'active'
            subscription.billing_cycle_end = datetime.now() + timedelta(days=30)
            subscription.grace_period_end = None
            subscription.save()
            # send_mail(
            #     'Subscription Activated',
            #     f'Dear {subscription.user.username},\nYour premium plan is now active until {subscription.billing_cycle_end.strftime("%Y-%m-%d")}.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [subscription.user.email],
            #     fail_silently=False,
            # )

        elif event['event'] == 'subscription.charged':
            subscription.status = 'active'
            subscription.billing_cycle_end = datetime.now() + timedelta(days=30)
            subscription.grace_period_end = None
            subscription.save()
            # send_mail(
            #     'Payment Successful',
            #     f'Dear {subscription.user.username},\nYour premium plan payment of ₹5000 was successful. Your subscription is active until {subscription.billing_cycle_end.strftime("%Y-%m-%d")}.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [subscription.user.email],
            #     fail_silently=False,
            # )

        elif event['event'] == 'subscription.paused':
            payment = event['payload'].get('payment', {}).get('entity', {})
            error_description = payment.get('error_description', 'Unknown error')
            error_reason = payment.get('error_reason', 'unknown')
            payment_method = payment.get('method', 'unknown')

            subscription.start_grace_period()
            grace_end = subscription.grace_period_end
            cancel_date = grace_end + timedelta(days=5)

            if payment_method == 'upi':
                error_message = {
                    'insufficient_funds': 'Your UPI payment failed due to insufficient funds. Please ensure your account has sufficient balance.',
                    'invalid_vpa': 'Your UPI payment failed due to an invalid VPA. Please verify your UPI ID.',
                }.get(error_reason, f'Your UPI payment failed: {error_description}. Please try again or use a different payment method.')
            elif error_reason == 'mandate_rejected':
                error_message = 'Your auto-pay mandate was rejected or disabled. Please re-enable auto-pay or update your payment method.'
            else:
                error_message = f'Your payment failed: {error_description}. Please update your payment method to continue your subscription.'

            # send_mail(
            #     'Payment Failed - Action Required',
            #     f'Dear {subscription.user.username},\n{error_message}\nYou have a 2-day grace period to resolve this by {grace_end.strftime("%Y-%m-%d %H:%M:%S")}. If unresolved, your subscription will be cancelled on {cancel_date.strftime("%Y-%m-%d %H:%M:%S")}.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [subscription.user.email],
            #     fail_silently=False,
            # )

        elif event['event'] == 'subscription.resumed':
            subscription.status = 'active'
            subscription.billing_cycle_end = datetime.now() + timedelta(days=30)
            subscription.grace_period_end = None
            subscription.save()
            # send_mail(
            #     'Subscription Resumed',
            #     f'Dear {subscription.user.username},\nYour premium plan has been resumed after a successful payment. Your subscription is active until {subscription.billing_cycle_end.strftime("%Y-%m-%d")}.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [subscription.user.email],
            #     fail_silently=False,
            # )

        elif event['event'] == 'subscription.pending':
            subscription.status = 'pending'
            subscription.save()
            # send_mail(
            #     'Payment Pending',
            #     f'Dear {subscription.user.username},\nYour premium plan payment is pending confirmation. We’ll notify you once it’s processed.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [subscription.user.email],
            #     fail_silently=False,
            # )

        elif event['event'] == 'subscription.halted':
            subscription.plan = '1'
            subscription.status = 'cancelled'
            subscription.razorpay_subscription_id = None
            subscription.billing_cycle_end = None
            subscription.grace_period_end = None
            subscription.save()
            # send_mail(
            #     'Subscription Cancelled',
            #     f'Dear {subscription.user.username},\nYour premium subscription has been cancelled due to repeated payment failures. You are now on the free plan.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [subscription.user.email],
            #     fail_silently=False,
            # )

        elif event['event'] == 'subscription.cancelled':
            subscription.status = 'cancelled'
            subscription.save()
            # send_mail(
            #     'Subscription Cancelled',
            #     f'Dear {subscription.user.username},\nYour premium subscription has been cancelled. You retain premium access until {subscription.billing_cycle_end.strftime("%Y-%m-%d")}.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [subscription.user.email],
            #     fail_silently=False,
            # )

        elif event['event'] == 'subscription.completed':
            subscription.plan = '1'
            subscription.status = 'cancelled'
            subscription.razorpay_subscription_id = None
            subscription.billing_cycle_end = None
            subscription.grace_period_end = None
            subscription.save()
            # send_mail(
            #     'Subscription Completed',
            #     f'Dear {subscription.user.username},\nYour premium subscription has completed its 12-month term. You are now on the free plan. Renew to continue premium access.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [subscription.user.email],
            #     fail_silently=False,
            # )

        elif event['event'] == 'subscription.updated':
            # Update relevant fields (e.g., plan_id, remaining_count)
            subscription.save()
            # send_mail(
            #     'Subscription Updated',
            #     f'Dear {subscription.user.username},\nYour premium subscription details have been updated. Please check your account for details.',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [subscription.user.email],
            #     fail_silently=False,
            # )

        return HttpResponse(status=200)
    except Subscription.DoesNotExist:
        return HttpResponse(status=404, content='Subscription not found')
    except razorpay.errors.SignatureVerificationError:
        return HttpResponse(status=400, content='Invalid webhook signature')
    except Exception as e:
        return HttpResponse(status=400, content=f'Error processing webhook: {str(e)}')