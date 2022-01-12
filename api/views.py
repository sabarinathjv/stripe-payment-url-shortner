from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.conf import settings
import stripe
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
from django.core.mail import send_mail
import requests
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"

class Invoices(APIView):

  
    def get(self, request, format=None):
        user = request.user.id
        return Response(data={},template_name="index.html")

    def post(self,request):
        try:
           
            invoice_id = request.data.get('invoice_id')
            client_name = request.data.get('client_name')
            client_email = request.data.get('client_email')
            project_name = request.data.get('project_name')
            amount = request.data.get('amount')
            invoice = Invoice.objects.create(number=invoice_id,name=client_name,email=client_email,project_name=project_name,amount=amount)
            invoice.save()
            YOUR_DOMAIN = "http://127.0.0.1:8000"
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': amount,
                            'product_data': {
                                'name': client_name,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "invoice_id": invoice.id
                },
                mode='payment',
                success_url=YOUR_DOMAIN + '/api/success/',
                cancel_url=YOUR_DOMAIN + '/api/cancel/',)
            url = "https://api-ssl.bitly.com/v4/shorten"
            headers = {
                "Host": "api-ssl.bitly.com",
                "Accept": "application/json",
                "Authorization": f"Bearer {settings.BITLY_TOKEN}"
            }
            payload = {
                "group_guid": settings.BITLY_GROUP_GUID,
                "long_url": checkout_session.url
            }
            res = requests.post(url, headers=headers, json=payload)
            short_url = res.json()[u'id']
            invoice.url = short_url
            invoice.save()
            subject = 'Your payment link'
            message = f'Hi please click here to payment {short_url}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [client_email]
            send_mail(subject, message , email_from ,recipient_list )   

            
            return Response(data={"data":"True","message":"Payment Mail successfully send"},status=status.HTTP_202_ACCEPTED)
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)


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

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        invoice_id = session["metadata"]["invoice_id"]
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.paid=True
        invoice.save()

    return HttpResponse(status=200)