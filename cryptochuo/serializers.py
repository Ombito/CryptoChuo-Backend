from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from cryptochuo.models import Customer



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["first_name","last_name","email","password","confirm_password"]


class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('first_name',"last_name", "email","password", "confirm_password")
        extra_kwargs = {"password": {"write_only": True}}
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs        
        
    def create(self, validated_data):
        customer = Customer.objects.create(validated_data["first_name"],
        validated_data["last_name"],
        validated_data["email"])
        customer.set_password(validated_data['password'])
        customer.save()
        return customer        