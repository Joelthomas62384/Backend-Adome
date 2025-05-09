
from django.contrib import admin
from django.urls import path
from . views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-courses' ,CourseListView.as_view() ),
    path('create-course' , CourseCreateView.as_view()),
    path('manage-course/<id>' , CourseManageView.as_view()),
    path('get-modules/<courseId>' , GetAllModules.as_view()),
    path('manage-modules/<id>' , ManageModules.as_view()),
    path('get-chapters/<id>' , GetAllChapters.as_view()),
    path('manage-chapters/<id>', ManageChapters.as_view()),
    path('create-chapter', ManageChapters.as_view()),
    path('preview-course/<id>' , CoursePreviewAPIView.as_view()),
    path('watch/course/<int:id>', CourseWatchViews.as_view(), ),
    path('my-courses' , MyCoursesView.as_view()),
    path('course-sales' , AllCoursesSalesView.as_view()),
    path('course-six-month' , SixMonthsCourseSales.as_view()),
    path('course-bought' ,CourseBoughtAnalytics.as_view() )
]



