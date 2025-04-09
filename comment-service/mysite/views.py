from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from app.models import Comment
from .serializers import CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

class CommentPagination(PageNumberPagination):
    page_size = 10

class CommentGetView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request, blogId):
        comments = Comment.objects.filter(contentType='blog', contentId=blogId, parent__isnull=True ).order_by('-created_at')
        
        paginator = CommentPagination()
        paginated_comments = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(paginated_comments, many=True)

        return paginator.get_paginated_response(serializer.data)



class CommentManageView(APIView):

    def post(self, request, blogId):
        import time
        time.sleep(5)
        print(request.user)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.tenantuser, contentId=blogId, contentType='blog')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, blogId):
        comment_id = request.data.get('id')
        if not comment_id:
            return Response({"detail": "Comment ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comment, id=comment_id, contentId=blogId)

        if comment.user != request.tenantuser:
            return Response({"detail": "You are not authorized to edit this comment."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Only update fields provided
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, blogId):
        comment_id = request.query_params.get('id')
        if not comment_id:
            return Response({"detail": "Comment ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comment, id=comment_id, contentId=blogId)

        if comment.user != request.tenantuser and not request.tenantuser.is_admin:
            return Response({"detail": "You are not authorized to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({"detail": "Comment deleted."}, status=status.HTTP_204_NO_CONTENT)