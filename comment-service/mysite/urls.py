
from django.urls import path
from .views import *
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('comments/<blogId>' , CommentGetView.as_view()),
    path('comments/manage/<blogId>' ,CommentManageView.as_view() )
]


