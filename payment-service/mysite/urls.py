
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gateway-register' , PaymentGatewayRegister.as_view()),
    path('create-order' , CreateCourseOrderView.as_view()),
    path('verify-order' , VerifyPayment.as_view())
]
