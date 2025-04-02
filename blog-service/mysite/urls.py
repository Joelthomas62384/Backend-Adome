
from django.contrib import admin
from django.urls import path
from .views import BlogView,BlogDetailView,GetblogView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog' , BlogView.as_view()),
    path('admin-blog',BlogDetailView.as_view()),
    path('blog-get/<pk>' , GetblogView.as_view()),
    path('blog/<pk>' , BlogDetailView.as_view()),
]
