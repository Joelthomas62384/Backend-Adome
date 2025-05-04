from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from rest_framework.response import Response
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from . import constants
from .scope_decorator import user_permission

from rest_framework import generics


class CoursePagination(PageNumberPagination):
    page_size = 10

class CourseListView(APIView):
    # authentication_classes = []
    permission_classes = []

    def get(self, request):
        courses = Course.objects.filter(tenant=request.tenant).order_by('-created_at')

        paginator = CoursePagination()
        paginated_courses = paginator.paginate_queryset(courses, request)

        serializer = CourseSerializer(paginated_courses, many=True , context={'request': request})
        return paginator.get_paginated_response(serializer.data)




class CourseCreateView(APIView):



    @user_permission(constants.HAS_COURSES_PERMISSION)
    def post(self, request):
        print("Working")
        serializer = CourseSerializer(data=request.data , context={'request': request})
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response(serializer.data , status=201)
        return Response(serializer.errors , status=400)



class CourseManageView(APIView):
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        serializer = CourseSerializer(course , context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def put(self, request, id):
        course = get_object_or_404(Course, id=id)
        serializer = CourseSerializer(course, data=request.data, partial=True , context={'request': request})  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def delete(self, request, id):
        course = get_object_or_404(Course, id=id)
        course.delete()
        return Response({'detail': 'Course deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class GetAllModules(APIView):

    def get(self, request, courseId):
        course = Course.objects.get(id = courseId)
        modules  = Module.objects.filter(course = course)
        serializer = ModuleSerializer(modules, many=True)
        print(serializer.data)
        return Response(serializer.data, status=200)


class ManageModules(APIView):
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def get(self, request, id):
        module = Module.objects.get(id=id)
        serializer = ModuleSerializer(module)
        return Response(serializer.data, status=200)
    
    def post(self , request, id):
        print(request.data)
        serializer = ModuleSerializer(data=request.data , context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status=400)
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def delete(self, request , id):
        try :
            module = Module.objects.get(id=id)
            print(module)
            module.delete()
            return Response({'detail': 'Module deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Module.DoesNotExist: 
            print("module not found")
            return Response({'detail': 'Module not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def put(self , request , id):
        try:
            module = Module.objects.get(id=id)
            serializer = ModuleSerializer(module, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Module.DoesNotExist:
            return Response({'detail': 'Module not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GetAllChapters(APIView):
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def get(self , request, id):
        chapters = Chapter.objects.filter(module__id=id)
        print(chapters)
        serializer = ChapterSerializer(chapters , many=True)
        return Response(serializer.data, status=200)
    

class ManageChapters(APIView):
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def get(self , request, id):
        chapter = Chapter.objects.get(id=id)
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data, status=200)
    
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def post(self, request):
        data = request.data
        print(data)
        serializer = ChapterSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def delete(self, request , id):
        try :
            chapter = Chapter.objects.get(id=id)
            print(chapter)
            chapter.delete()
            return Response({'detail': 'Chapter deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Chapter.DoesNotExist: 
            print("chapter not found")
            return Response({'detail': 'Chapter not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def put(self , request , id):
        try:
            chapter = Chapter.objects.get(id=id)
            serializer = ChapterSerializer(chapter, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        except Chapter.DoesNotExist:
            return Response({'detail': 'Chapter not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

class CoursePreviewAPIView(generics.RetrieveAPIView):
    # authentication_classes = []
    permission_classes = []
    queryset = Course.objects.prefetch_related('module_set__chapter_set')
    serializer_class = CoursePreviewSerializer
    lookup_field = 'id'  
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request 
        return context
    





class CourseWatchViews(APIView):
    # authentication_classes = []
    # permission_classes = []
    def get(self, request, id):
        if not OwnedCourse.objects.filter(user =request.tenantuser , course__id=id).exists():
            return Response({'detail': 'You are not enrolled in this course.'}, status=status.HTTP_403_FORBIDDEN)
        course = Course.objects.prefetch_related('module_set__chapter_set').get(id=id)
        serializer = CourseWatchSerializer(course , context={'request': request})
        return Response(serializer.data)


class MyCoursesView(APIView):
    # authentication_classes = []
    # permission_classes = []
    def get(self, request):
        owned_courses = OwnedCourse.objects.filter(user=request.tenantuser)
        serializer = OwnedCourseSerializer(owned_courses, many=True , context={'request': request})
        return Response(serializer.data)