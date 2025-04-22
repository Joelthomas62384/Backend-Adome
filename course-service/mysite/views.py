from rest_framework.views import APIView
from rest_framework import status
from app.models import *
from rest_framework.response import Response
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from . import constants
from .scope_decorator import user_permission




class CoursePagination(PageNumberPagination):
    page_size = 10

class CourseListView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        courses = Course.objects.filter(tenant=request.tenant).order_by('-created_at')

        paginator = CoursePagination()
        paginated_courses = paginator.paginate_queryset(courses, request)

        serializer = CourseSerializer(paginated_courses, many=True)
        return paginator.get_paginated_response(serializer.data)




class CourseCreateView(APIView):



    @user_permission(constants.HAS_COURSES_PERMISSION)
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response(serializer.data , status=201)
        return Response(serializer.errors , status=400)



class CourseManageView(APIView):
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def put(self, request, id):
        course = get_object_or_404(Course, id=id)
        serializer = CourseSerializer(course, data=request.data, partial=True)  
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
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status=400)



class GetAllChapters(APIView):
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def get(self , request, id):
        chapters = Chapter.objects.filter(module__id=id)
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
        serializer = ChapterSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
        
    