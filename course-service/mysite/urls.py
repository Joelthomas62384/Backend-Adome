
from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-courses' ,CourseListView.as_view() ),
    path('create-course' , CourseCreateView.as_view())
]
