from rest_framework.views import APIView
from rest_framework import status
from app.models import Course
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
        serializer = CourseSerializer(course, data=request.data, partial=True)  # Use `partial=True` if you want to allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @user_permission(constants.HAS_COURSES_PERMISSION)
    def delete(self, request, id):
        course = get_object_or_404(Course, id=id)
        course.delete()
        return Response({'detail': 'Course deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
