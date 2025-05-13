
from django.contrib import admin
from django.urls import path
from .views import *
from .subscription_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gateway-register' , PaymentGatewayRegister.as_view()),
    path('create-order' , CreateCourseOrderView.as_view()),
    path('verify-order' , VerifyPayment.as_view()),
    path('get-wallet' , WalletDetailsInAnalytics.as_view()),
    path('six-months-analytics' , TotalOrdersWeGotInSixMonths.as_view()),
    path('seven-day-analytics' , TotalOrdersWeGotInSevenDays.as_view()),
    path('previous-orders' ,PreviousOrderLogs.as_view()),
    path('check-connected',CheckConnectedPayment.as_view() )

]
