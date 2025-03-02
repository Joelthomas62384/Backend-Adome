
from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tenant' , TenantView.as_view()),
    path('tenant/<subdomain>' , TenantView.as_view()),
    path('metadata' , MetadataView.as_view()),
    
]


