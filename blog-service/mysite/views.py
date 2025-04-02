from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination



class BlogPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100
class BlogView(APIView):
    authentication_classes = []
    permission_classes  = []
    def get(self, request):
      

        blogs = Blog.objects.filter(tenant=request.tenant, published=True)
        paginator = BlogPagination()
        paginated_blogs = paginator.paginate_queryset(blogs, request)

        serializer = BlogSerializer(paginated_blogs, many=True)
        return paginator.get_paginated_response(serializer.data)

class BlogDetailView(APIView):
    def get(self, request):
        all_posts = request.GET.get('all_posts','false').lower() == 'true'

        blogs = Blog.objects.filter(tenant=request.tenant, )
        paginator = BlogPagination()
        paginated_blogs = paginator.paginate_queryset(blogs, request)

        serializer = BlogSerializer(paginated_blogs, many=True , context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.tenantuser, tenant =request.tenant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        blog = Blog.objects.filter(tenant=request.tenant, pk=pk).first()
        if not blog:
            return Response({'data': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        blog = Blog.objects.filter(tenant=request.tenant, pk=pk).first()                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        if not blog:
            return Response({'data': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        blog.delete()
        return Response({'data': 'Blog deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class GetblogView(APIView):
    def get(self, request, pk):
        blog = Blog.objects.filter(tenant=request.tenant, pk=pk).first()
        if not blog:
            return Response({'data': 'Blog not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogSerializer(blog, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)




