from django.urls import path,include
from rest_framework import routers
from cryptochuo.views import CustomerViewSet
from . import views

router = routers.DefaultRouter()
router.register(r"signup",CustomerViewSet)


urlpatterns=[
    path("",include(router.urls)),
    # path('signup/', views.CustomerRegisterSerializer,name='signup'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))




]
