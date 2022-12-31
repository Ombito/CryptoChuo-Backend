from django.urls import path,include
from rest_framework import routers
from cryptochuo.views import UserViewSet
from . import views

router = routers.DefaultRouter()
# router.register(r"signup",UserViewSet)


urlpatterns=[
    path("",include(router.urls)),
    path('signup/', views.UserRegisterSerializer,name='signup'),




]
