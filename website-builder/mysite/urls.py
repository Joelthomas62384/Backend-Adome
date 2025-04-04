
from django.contrib import admin
from django.urls import path
from . views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('website' ,WebsiteApiView.as_view() ),
    path('website/<id>' ,WebsiteApiView.as_view() ),
    path('builder-element/<id>' ,GetWebsiteView.as_view() ),
    path('tenant-default-website' , GetTenantDefaultWebpage.as_view())
    
]
