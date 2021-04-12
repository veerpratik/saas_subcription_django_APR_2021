
from rest_framework import serializers
from common_account.models.manager import Manager
from common_account.models.user import User
class ManagerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only = True)

    class Meta:
        model = Manager
        fields = (
            'id', 'first_name','last_name','date_of_birth','company',
            'address','created_date','updated_date', 'email', 'password'
        )

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        try:
             user = User.objects.create_manager(email=email, password=password)
        except:
            raise serializers.ValidationError("this email is already exists")
        validated_data['user'] = user
    
        return Manager.objects.create(**validated_data)