from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
import json
from djstripe.models import Product
import djstripe
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from common_account import constants



class Checkout(APIView):
    """
    List all Product, 
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        context_data = dict()
        products = Product.objects.all().values()
        queryset = Product.objects.all()
        books = []
        l = list()
        for obj in queryset:


            for plan in obj.plan_set.all():
            
                d = {'human_readable_price':plan.human_readable_price,
                    'id':plan.id}

                books.append(d)
                

        context_data[constants.RESPONSE_RESULT] = books
        context_data[constants.RESPONSE_RESULT2] = list(products)
        return Response( context_data)



class Create_sub(APIView):
    '''
    create subcription and fetch that data to the DB

    '''
    def post(self, request, format=None):
        
        # Reads application/json and returns a response
        data = json.loads(request.body)
        payment_method = data['payment_method']
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

        try:
            # This creates a new Customer and attaches the PaymentMethod in one API call.
    
            customer = stripe.Customer.create(
                payment_method=payment_method,
                email= request.user.email,
                invoice_settings={
                    'default_payment_method': payment_method
                }
            )

            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
            request.user.customer = djstripe_customer
            

            # At this point, associate the ID of the Customer object with your
            # own internal representation of a customer, if you have one.
        

            # Subscribe the user to the subscription created
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": data["price_id"],
                    },
                ],
                expand=["latest_invoice.payment_intent"]
            )

            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

            request.user.subscription = djstripe_subscription
            request.user.save()
 

            return Response(subscription)
        except Exception as e:
            return Response({'error': (e.args[0])}, status =403)

class Cancel_sub(APIView):
    """
    Cancel Subcription.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        context_data = dict()
  
        sub_id = request.user.subscription.id

        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        try:
            stripe.Subscription.delete(sub_id)
        except Exception as e:

            return Response({'error': (e.args[0])}, status =403)
         
        
        context_data[constants.RESPONSE_MESSAGE] = "Subcription has been cancelled" 
        return Response(context_data)    




