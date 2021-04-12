from django.urls import path
from common_account.views import manager_views


urlpatterns = [

    path("checkout/", manager_views.Checkout.as_view(), name="checkout"),
    path("create-sub/", manager_views.Create_sub.as_view(), name="create sub"), 
     
    
   
]
