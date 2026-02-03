import stripe
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from config import settings
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


@extend_schema(tags=['Payment'])
class CreateCheckoutSessionView(APIView):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'KGS',
                            'product_data': {
                                'name': 'Payment asiya',  # Название заказа или продукта
                            },
                            'unit_amount': int(order.total_price * 100),  # Цена в центах
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                metadata={
                    "order_id": order.id
                },
                success_url=settings.PAYMENT_SUCCESS_URL,  # URL после успешной оплаты
                cancel_url=settings.PAYMENT_CANCEL_URL,    # URL после отмены оплаты
            )
            return Response({
                'checkout_url': checkout_session.url
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Payment'])
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        order_id = session.metadata.get('order_id')

        if order_id:
            order = Order.objects.get(id=order_id)
            order.status = Order.Status.PAID

            order.save()

    return HttpResponse(status=200)
