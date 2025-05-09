
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-communities' ,GetCommunitiesUser.as_view()),
    path('get-messages/<id>' , GetMessages.as_view() )
]
