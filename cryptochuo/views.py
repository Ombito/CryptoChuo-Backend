# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = serializers.RegisterSerializer
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         student = serializer.save()
#         User.objects.create_user(username=student.username , password=student.password)
#         return Response({
#         "student": serializers.StudentSerializer(student, context=self.get_serializer_context()).data,
#         # "token": AuthToken.objects.create(student)[1]
#         })
# class LoginAPI(ObtainAuthToken):
#     permission_classes = (permissions.AllowAny,)
#     def post(self, request, format=None):
#         username=request.data['username']
#         password=request.data['password']
#         user=authenticate(request,username=username, password=password)
#         print(user)
#         token=Token.objects.create(user=user)
#         return Response({
#             'body': 'login successful',
#             "token": token.key
#         })


from django.shortcuts import render
from . import serializers
# Create your views here.
# from django.contrib.auth.models import Customer
from rest_framework import viewsets
from rest_framework import permissions
# from views import UserSerializer

from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets 
from cryptochuo.serializers import CustomerSerializer,CustomerRegisterSerializer
from cryptochuo.models import Customer
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, permissions
# from django.contrib.auth import login,authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status
# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    
    def register_user(request):
        if request.method == "POST":
            serializer = CustomerRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201) 


                