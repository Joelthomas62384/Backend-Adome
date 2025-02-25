
from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tenant' , TenantView.as_view()),
    path('tenant/<id>' , TenantView.as_view()),
    
]


