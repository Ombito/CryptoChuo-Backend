from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from cryptochuo.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","password","confirm_password"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name',"last_name", "email","password", "confirm_password")
        extra_kwargs = {"password": {"write_only": True}}
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs        
        
    def create(self, validated_data):
        user = User.objects.create(validated_data["first_name"],
        validated_data["last_name"],
        validated_data["email"])
        user.set_password(validated_data['password'])
        user.save()
        return user        