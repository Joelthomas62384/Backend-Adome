
from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login' , LoginView.as_view()),
    path('refresh' , RefreshTokenView.as_view()),
    path('data-login' , LoginDataView.as_view()),
    path('logout' , LogoutView.as_view()),
    path('me' , GetUserView.as_view()),
    path('tenantusers' , GetTenantUsersView.as_view()),
    path('tenantuser' , GetTenantUserView.as_view()),
    path('ban/<username>',BanUserView.as_view()),
    path('block/<username>',BanUserView.as_view())
]
