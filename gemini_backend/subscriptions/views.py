import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework import status
from .models import Subscription
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import HttpResponse
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

class ProSubscription(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            # Create Stripe customer if not exists
            subscription, created = Subscription.objects.get_or_create(user=user)
            if not subscription.stripe_customer_id:
                customer = stripe.Customer.create(email=user.email)
                subscription.stripe_customer_id = customer.id
                subscription.save()

            # Create Checkout Session
            checkout_session = stripe.checkout.Session.create(
                customer=subscription.stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price': settings.STRIPE_PRO_PRICE_ID,  # This is the price_id from Stripe dashboard
                    'quantity': 1,
                }],
                mode='subscription',
                success_url=settings.DOMAIN + '/payment/success/',
                cancel_url=settings.DOMAIN + '/subscription/pro/',
                metadata={
                    'user_id': str(user.id),  # Send user id for later retrieval
                }
            )
            return Response({"checkout_url": checkout_session.url},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StripeWebhook(APIView):
    permission_classes = []  # Allow unauthenticated Stripe POST
    authentication_classes = []  # Disable auth middleware

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        event_type = event['type']
        data = event['data']['object']

        if event_type in ['customer.subscription.created', 'customer.subscription.updated']:
            customer_id = data['customer']
            stripe_sub_id = data['id']
            sub_end = data.get('current_period_end')
            status = data.get('status')  # optional: check if it’s 'active' or 'canceled'

            try:
                sub = Subscription.objects.get(stripe_customer_id=customer_id)
                sub.stripe_subscription_id = stripe_sub_id
                sub.plan = 'pro' if status == 'active' else 'basic'
                sub.is_active = status == 'active'
                sub.end_date = timezone.datetime.fromtimestamp(sub_end) if sub_end else None
                sub.save()
            except Subscription.DoesNotExist:
                pass

        elif event_type == 'customer.subscription.deleted':
            customer_id = data['customer']
            try:
                sub = Subscription.objects.get(stripe_customer_id=customer_id)
                sub.plan = 'basic'
                sub.is_active = False
                sub.stripe_subscription_id = None
                sub.end_date = None
                sub.save()
            except Subscription.DoesNotExist:
                pass

        return HttpResponse(status=200)

class SubscriptionStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sub = Subscription.objects.get(user=request.user)
            return Response({
                "plan": sub.plan,
                "active": sub.is_active,
                "valid_until": sub.end_date
            })
        except Subscription.DoesNotExist:
            return Response({"plan": "basic", "active": False})

class PaymentSuccess(APIView):
    def get(self,request):
        return Response({'message':'Payment Success enjoy pro'})