
from django.urls import path
from .views import *

urlpatterns = [
      path('invoice', Invoices.as_view(), name='invoice'),
      path('cancel/', CancelView.as_view(), name='cancel'),
      path('success/', SuccessView.as_view(), name='success'),
      path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),



      

]
