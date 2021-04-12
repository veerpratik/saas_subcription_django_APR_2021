

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.email
        return token
   

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common_account.models.manager import Manager
from common_account.serializers import ManagerSerializer
from common_account import constants
from rest_framework import status


class Singnup(APIView):
    """
    create a new user.
    """
    def post(self, request, format=None):
        context_data = dict()
        data = request.data
        error = False
        msg = ''

        email = data.get('email', None)
        first_name = data.get('first_name', None)
        company = data.get('company', None)
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if not email:
            error = True
            msg = 'email is required'
        if not error and not  first_name:
            error = True
            msg = ' first_name is required'
        if not error and not  company:
            error = True
            msg = ' company is required'
        if not error and not password:
            error = True
            msg = "Password is required."     
        if not error and not confirm_password:
            error = True
            msg = "confirm_password is required."
        if not error and password != confirm_password:
            error = True
            msg = 'Password mismatch'    

        if not error:
            obj  = Manager.objects.filter(user__email = email).first()
            if obj:
                context_data[constants.RESPONSE_ERROR] = True
                context_data[constants.RESPONSE_MESSAGE] = 'This email has already registered'
                return Response(context_data)
  

            serializer = ManagerSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                context_data[constants.RESPONSE_RESULT] = serializer.data
                context_data[constants.RESPONSE_ERROR] = False
                context_data[constants.RESPONSE_MESSAGE] = 'New User added successfully.'
                return Response(context_data)
               
            else:

                context_data[constants.RESPONSE_ERROR] = True
                context_data[constants.RESPONSE_MESSAGE] = serializer.errors
                
        else:

            context_data[constants.RESPONSE_ERROR] = True
            context_data[constants.RESPONSE_MESSAGE] = msg
        return Response(context_data, status=status.HTTP_400_BAD_REQUEST)

